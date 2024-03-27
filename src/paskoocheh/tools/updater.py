# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for Iranian
#
# Copyright (C) 2024 ASL19 Organization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import hashlib
import pytz
import socket
import requests
import logging
import time
import math
import zipfile
from datetime import datetime
from pyaxmlparser import APK as apk_parser
from tools.tools_settings import TOOLS_PATH, SPLITS_PATH
from django.conf import settings
from django.core.files import File
from tempfile import SpooledTemporaryFile
from tools.libs.gpapi.googleplay import GooglePlayAPI
from tools.models import Version, AndroidSplitFile, VersionCode
from preferences.models import (
    GooglePlayApiPreference,
    PaskoochehAndroidPreference,
    GeneralPreference,
    AndroidDeviceProfile,
)
from paskoocheh.email import Email
from operator import attrgetter

MAX_NUMBER_OF_RETRIES = 2
MAX_NUMBER_OF_RETRY_TOKENS = 2
MAX_NUMBER_OF_DOWNLOAD_RETRIES = 1
ABI_SPLIT_TYPES = ['arm64_v8a', 'armeabi_v7a', 'armeabi', 'x86_64', 'x86']

logger = logging.getLogger('updater')


class Updater(object):
    """
        Class to download latest versions of
        apps either from google store or their
        download_url
    """

    def __init__(self):
        self.messages = []

        # Google Play API client
        self.api = None

        # If the client is logged in and healthy
        self.logged_in = False

        # The device codename and name used to login to the Google Play Store API
        self.device_codename = None
        self.device_name = None

    def first_login(self, user, password):
        """
            Login to Google Play Store without a token
        """

        try:
            self.api.login(user, password, None, None)
        except Exception as e:
            logger.error(f"[ERROR] The Login to Google Play Store has failed ({e})")
            return -1

        return 0

    def login(self, device_codename="walleye"):  # noqa C901 Defaults to Google Pixel 2
        """
            Login to the Google Play API

            Returns:
            True if successful, False otherwise
        """

        prefs = GooglePlayApiPreference.objects.get()
        if not prefs.android_id or not prefs.google_user or not prefs.google_pass:
            msg = '[ERROR] Google Play API preferences are not set'
            logger.error(msg)
            self.messages.append(msg)
            return -1

        self.api = GooglePlayAPI(
            locale='en_US', timezone='America/New_York', device_codename=device_codename)
        if self.api is None:
            msg = '[ERROR] Unable to create GooglePlayApi object'
            logger.error(msg)
            self.messages.append(msg)
            return -1

        token = prefs.token
        if not token:
            msg = f"[INFO] Logging in as [{self.device_name} | {self.device_codename}] device..."
            logger.info(msg)
            self.messages.append(msg)

            logger.info(
                'Logging to the Google Play API without a token to fetch a new token...')
            rc = self.first_login(prefs.google_user, prefs.google_pass)
            if rc != 0:
                return rc

            logger.info('A new token was successfully obtained!')
            token = self.api.authSubToken
            if token is None:
                msg = "[ERROR] Unable to obtain a new token"
                logger.error(msg)
                self.messages.append(msg)
                return -1

            prefs.android_id = self.api.gsfId
            prefs.token = token

            prefs.save()

        retry_token = 0

        while (retry_token < MAX_NUMBER_OF_RETRY_TOKENS):
            try:
                self.api.login(None, None, int(prefs.android_id), token)
            except Exception as e:
                # Set token to None to fetch a new one
                # on the second trial
                prefs.token = None
                prefs.save()
                token = prefs.token

                msg = f"[ERROR] Logging in to the google API has failed (error={e}). " \
                    "Login token has probably expired.\nTrying again..."
                logger.error(msg)
                self.messages.append(msg)

                retry_token += 1
                break

            retry = 0
            while (retry < MAX_NUMBER_OF_RETRIES):
                try:
                    self.api.search(query='chrome')
                except Exception as e:
                    msg = f"[ERROR] Checking token validation failed (error={e}). " \
                        "Google Play Store Token has probably expired (Try again)."
                    logger.error(msg)
                    self.messages.append(msg)
                return 0

            retry_token += 1
            try:
                rc = self.first_login(
                    prefs.google_user, prefs.google_pass, prefs.android_id)
            except Exception as e:
                logger.error(f"[ERROR] logging in to the google API has failed due to: {e}")
            if rc != 0:
                return rc

            token = self.api.authSubToken
            if token is None:
                logger.error("[ERROR] Unable to refresh token")
                return -1

            prefs.android_id = self.api.gsfId
            prefs.token = token

            prefs.save()

            time.sleep(1)
            continue

        return -2

    def update_apks(self):      # noqa C901
        """
            Updates an android apk from playstore or
            the url
        """

        devices = AndroidDeviceProfile.objects \
            .filter(status='completed') \
            .order_by('id') \

        android_tools = Version.objects \
            .filter(supported_os__slug_name='android') \
            .filter(auto_update=True) \
            .select_related('tool') \
            .order_by('release_date') \
            .all()

        prefs = GooglePlayApiPreference.objects.get()

        platform = (settings.PLATFORM).capitalize()

        msg = f"[INFO] {platform} has [{len(devices)}] Android device profiles and " \
            f"[{len(android_tools)}] apps set for auto-update.\n"
        logger.info(msg)
        self.messages.append(msg)

        updated_apps = []
        updated_bundled_apps = []
        retry_again = False
        retry = 0
        while retry < MAX_NUMBER_OF_DOWNLOAD_RETRIES:

            # Login to Google Play Store as each device
            for i, device in enumerate(devices, start=1):
                if not device.codename or not device.name:
                    msg = '[ERROR] Android device profiles on the admin panel are not set yet.'
                    logger.error(msg)
                    return
                else:
                    self.device_codename = device.codename
                    self.device_name = device.name
                    msg = f"\n<<< [{i}] {self.device_name} ({self.device_codename}) >>>\n"
                    logger.info(msg)
                    self.messages.append(msg)

                    if not self.logged_in:
                        logger.warning(f"Not logged in, logging in as [{self.device_name} | {self.device_codename}]")
                        retry_again = True
                        rc = self.login(self.device_codename)
                        if rc < 0:
                            msg = f"[ERROR] Unable to login to google as [{self.device_codename}]. " \
                                "Unlocking the account might be needed from: " \
                                "https://accounts.google.com/b/0/DisplayUnlockCaptcha"
                            logger.error(msg)
                            self.messages.append(msg)
                            time.sleep(2)
                            continue
                        self.logged_in = True

                    # update each android version
                    for j, tool in enumerate(android_tools, start=1):
                        toolname = tool.tool.name
                        if tool.tool.publishable is False:
                            continue
                        # TODO: since we have to add each device to their respected version code,
                        # we have to run the download tool part, check whether this can be optimized or not?
                        # if (toolname in updated_apps and tool.is_bundled_app is False):
                        #     msg = f"[INFO] [{toolname}] is an unbundled app that has already been " \
                        #         "updated from a previous device. No need to update it again!"
                        #     logger.info(msg)
                        #     self.messages.append(msg)
                        #     continue

                        logger.info(f"### [{j}] {toolname} ###\n"
                                    f"=> Attempting to update the existing version of {toolname} ...")
                        app = self.download_tool(tool)
                        if app:
                            updated_apps.append(toolname)
                        if app and tool.is_bundled_app:
                            updated_bundled_apps.append(tool)
                        time.sleep(1)

                    if retry_again:
                        retry_again = False
                        retry += 1

                    # Login token needs to be reset and 'logged_in' needs to be False to enable
                    # logging in as another device on the next device loop run with a fresh token
                    self.logged_in = False
                    prefs.token = None
                    prefs.save()
                    time.sleep(5)

        if len(updated_bundled_apps) > 0:
            msg = "\n[INFO] Updating for all devices has finished. Moving on to zipping (bundling) updated bundled apps..."
            logger.info(msg)
            self.messages.append(msg)

            # Remove duplicate apps
            updated_bundled_apps = list(set(updated_bundled_apps))

            # Bundle (zip) all collected splits along with
            # the base APK for each version codes for each updated bundled app
            for bundled_app in updated_bundled_apps:
                version_codes = VersionCode.objects.filter(version=bundled_app)
                for version_code_obj in version_codes:
                    zf = self.create_bundle(bundled_app, version_code_obj)
                    size = zf.tell()
                    logger.info(f"Size of zip file = {size}")
                    if size > 0:
                        appname = bundled_app.tool.get_app_name()
                        filename = f"{appname}/{settings.ANDROID_PREFIX}{version_code_obj.version_code}/{appname}-android.zip"
                        filepath = f"{TOOLS_PATH}{filename}"
                        logger.info(f"Zip file path: {filepath}")

                        version_code_obj.size = size
                        version_code_obj.uploaded_file.name = filepath
                        # This save will calculate the PGP signature and checksum
                        # for the bundled app based on the zip file
                        version_code_obj.uploaded_file.save(
                            filepath, File(zf), save=True)

                        extension = version_code_obj.uploaded_file.name.split(
                            '.')[-1].lower()
                        if version_code_obj.uploaded_file.storage.exists(version_code_obj.uploaded_file.name) and extension == 'zip':
                            msg = f"\t[INFO] Zip file (bundle) has been created successfully: [{version_code_obj.uploaded_file.name}]"
                            logger.info(msg)
                        else:
                            msg = f"\t[ERROR] Unable to create Zip file (bundle) for [{bundled_app.tool.name}] and version code [{version_code_obj.version_code}]!"
                            logger.error(msg)

                        self.messages.append(msg)

        # remove duplicate elements
        updated_apps = list(set(updated_apps))

        # send summary email
        self.conclude(updated_apps, self.messages)

        prefs.token = None
        prefs.save()

    @staticmethod
    def create_bundle(bundled_app, version_code):
        """
            Create a zip file (bundle) for a bundled app.
            The zip file will have the base APK along with
            all collected splits (from all devices)
            bundled into a zip file

            Args:
            bundled_app: A bundled app object (Version object)

            Returns:
            A zip file (bundle) as a SpooledTemporaryFile
        """
        toolname = bundled_app.tool.name
        logger.info(f"[INFO] Zipping the base apk along with all splits for [{toolname}] and version code [{version_code.version_code}]...")

        base = version_code.uploaded_file
        logger.info(f"[INFO] base.apk = {base}")

        splits = [obj.split_file for obj in AndroidSplitFile.objects.filter(
            version=bundled_app, tool_version_code=version_code)]

        # Removing duplicate splits if any
        splits = list(set(splits))

        # Add the base to the splits list
        splits.append(base)

        temp = SpooledTemporaryFile(max_size=60000000)  # 60 MB
        added_types = []

        # Writing files to a zipfile
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as zip:
            # Writing each file one by one (base + splits)
            for apk in splits:
                arcname = apk.name.split('/')[-1]
                split_type = arcname.split('.')[1]

                # This will ensure that there is always ONLY one split for each
                # split type (e.g. No 2 versions of arm64_v8a.apk) written in
                # the zip file, otherwise, the zip file will not be installable
                if split_type in added_types:
                    continue

                # Ensure that the largest split variation will be picked
                # as it is needed to make the zip file installable for all devices
                # regardless of the 'extractNativeLibs' value of the AndroidManifest.xml
                # of the base.apk
                if split_type in ABI_SPLIT_TYPES:
                    variations = [
                        split for split in splits if split_type in split.name]

                    if len(variations) > 0:
                        apk = max(variations, key=attrgetter('size'))
                        arcname = apk.name.split('/')[-1]

                logger.info(f"Zipping [{apk.name}] as [{arcname}]...")

                if settings.BUILD_ENV == 'local':
                    apk_path = f"{settings.MEDIA_ROOT}/{apk.name}"
                    zip.write(apk_path, arcname)
                else:
                    # HTTP GET the apk from S3 and then create a file
                    # out of the content (data) of the response
                    # into the zip file
                    r = requests.get(apk.url)
                    if r.status_code == 200:
                        zip.writestr(arcname, r.content)
                    else:
                        logger.error(f"Zipping [{apk.name}] as [{arcname}] has failed!")

                added_types.append(split_type)

        temp.flush()

        return temp

    @staticmethod
    def download_file(url, tempfile):
        """
            Download a file from a URL

            Args:
            url: the URL to download from
            tempfile: a file object to store the content

            Returns:
            checksum of the file in case of success, None otherwise
        """
        if not tempfile:
            return None

        hasher = hashlib.sha256()
        r = requests.get(url)
        if r.status_code == 200:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:       # filter out keep-alive new chunks
                    hasher.update(chunk)
                    tempfile(chunk)

            tempfile.flush()
            return hasher.hexdigest()

        return None

    @staticmethod
    def send_mail(subject, messages, from_addr, to_addr):
        """
            Send an email using SES

            Args:
            subject: Subject of email
            message: Body of email
            from_addr: From address
            to_addr: List of To addresses
        """

        email = Email(
            to=to_addr,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        email.subject(subject)
        email.text(messages)
        email.send(from_addr=from_addr)

    @staticmethod
    def send_update_email(app_list, to_list, messages):
        """
            Send notification update to admin
            to inform about the apps that were updated

            Args:
            app_list: List of apps that were updated
        """
        general_settings = GeneralPreference.objects.get()
        if not general_settings.from_email:
            msg = "[ERROR] From Email in General Settings (Admin Panel) is not set yet."
            logger.error(msg)
        else:
            subject = 'Updated Applications'
            server = socket.gethostbyname(socket.gethostname())
            message = messages + '\n\n'
            if app_list and len(app_list) > 0:
                app_list_line_joined = '\n'.join(app_list)
                message += f"Here is a list of updated applications from server ({str(server)}): \n{app_list_line_joined}"
            from_addr = general_settings.from_email
            to_addr = to_list

            Updater.send_mail(subject, message, from_addr, to_addr)

    @staticmethod
    def conclude(updated_apps, messages):
        """
            Send a summary of updated apps and log messages

            Args:
            updated_apps: List of apps that were updated
            messages: List of all log messages
        """

        emails = PaskoochehAndroidPreference.objects.get()
        if not emails.android_update_emails:
            msg = "[ERROR] Android Apps preferences is not set"
            logger.error(msg)
            messages.append(msg)
        else:
            email_list = str(emails.android_update_emails).split(',')
            if len(email_list) > 0:
                logger.info(f"\n*********************SUMMARY*********************\n"
                            f"Updated apps: {updated_apps}")
                updated_app_count_msg = f"Number of updated apps: {len(updated_apps)}"
                logger.info(updated_app_count_msg)
                messages.append(updated_app_count_msg)

                messages = '\n'.join(messages)

                logger.info(f"Collected messages:\n{messages}\n"
                            f"Sending out update email ...")
                try:
                    Updater.send_update_email(
                        updated_apps, email_list, messages)
                except Exception as e:
                    logger.error(f"[ERROR] Unable to send summary email due to: {e}")
            else:
                logger.error(
                    "[ERROR] Android Apps email preferences should be comma separated values")

    def convert_size(self, size_bytes):
        """
            Convert a size in bytes (int) to a readable
            format with a unit

            Args:
            size_bytes: The size number in bytes (int)

            Returns:
            A string containing the calculated size with its unit
        """

        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def write_temp_file_to_memory(self, data, max_size=50000000):
        """
            Write file data into a temporary file in memory

            Args:
            data: The data to be written into a temporary file
            max_size: The size of the file to be created
                in memory in bytes with a default of 50 MB

            Returns:
            The temporary file created in memory
        """

        temp = SpooledTemporaryFile(max_size=max_size)

        # Write temp file in memory
        for chunk in data:
            temp.write(chunk)
        temp.flush()

        return temp

    def get_latest_from_url(self, tool):
        """
            Download the latest APK from a URL

            Args:
            tool: Version object containing the version info
            filename: The target filename to upload to db

            Returns:
            True if the tool is updated, False otherwise
        """
        if not tool.download_url:
            msg = f'[ERROR] Release URL is not set for tool {tool}'
            logger.error(msg)
            self.messages.append(msg)
            return False

        temp = SpooledTemporaryFile(max_size=153600)
        checksum = Updater.download_file(tool.download_url, temp)
        if checksum is None:
            msg = f'[ERROR] Error in downloading file for tool {tool}'
            logger.error(msg)
            self.messages.append(msg)
            return

        downloaded_apk = apk_parser.APK(temp.name)
        ver_str = downloaded_apk.get_androidversion_name()
        ver_code = int(downloaded_apk.get_androidversion_code())
        permissions = ','.join(downloaded_apk.get_permissions())
        size = os.fstat(temp.fileno()).st_size
        rel_date = datetime.now()
        rel_date = pytz.timezone('Iran').localize(rel_date, is_dst=None)

        logger.info(f'\tversionString = {ver_str}')
        logger.info(f'\tversionCode = {ver_code}')
        logger.info(f'\treleaseDate = {rel_date}')
        logger.info(f'\tpermissions = {permissions}')

        # checking tool version first, if not same then
        # updating new version name in existing one and deleting versionCode objects related to it, updating release date
        if tool.version_number != ver_str:
            msg = f"[INFO] Updating version for {tool} to version = ({ver_str})..."
            logger.info(msg)
            # deleting VersionCode objects related to existing Version(tool) object and setting new version name
            msg = f"[INFO] Deleting version code objects for {tool} | Version ({tool.version_number}) ..."
            logger.info(msg)
            VersionCode.objects.filter(version=tool).delete()
            tool.version_number = ver_str
            tool.release_date = rel_date
            tool.last_modified = rel_date
            tool.save()

        # create a VersionCode if not found for given versionName
        version_code_obj, vc_created = VersionCode.objects.get_or_create(
            version=tool,
            version_code=ver_code
        )

        # adding device to the version code object
        logger.info(f"Adding the current device [{self.device_codename}] to the devices of version code [{version_code_obj.version_code}]...")
        try:
            version_code_obj.devices.add(
                AndroidDeviceProfile.objects.get(codename=self.device_codename))
            version_code_obj.save()
        except Exception as e:
            logger.error(f"Unable to add the current device to the devices of the version code [{version_code_obj.version_code}] due to:\n{e}")

        # checking if version code already exists or not
        if not vc_created:
            msg = f"[INFO] {tool} with version code {version_code_obj.version_code} and version ({ver_str}) is up-to-date "
            logger.info(msg)
            self.messages.append(msg)
            return False

        logger.warning(f"Version code = {str(version_code_obj.version_code)} created")
        logger.warning(f"Updating tool {tool.tool.name} ...")

        # Delete the existing apk to prevent duplicate apk files
        # per version on S3 and to always have accurate
        # checksums and signatures based on one file only
        # as overwriting the file is disabled
        filename = TOOLS_PATH + f"{tool.tool.get_app_name()}/{settings.ANDROID_PREFIX}{version_code_obj.version_code}/{tool.tool.get_app_name()}-android.apk"
        if not vc_created:
            if version_code_obj.uploaded_file.storage.exists(filename):
                version_code_obj.uploaded_file.storage.delete(filename)

        version_code_obj.uploaded_file.save(filename, File(temp), save=False)
        version_code_obj.uploaded_file.name = filename
        version_code_obj.checksum = checksum
        version_code_obj.size = size
        version_code_obj.save()

        # Updating tool
        tool.permissions = permissions
        tool.last_modified = rel_date
        tool.save()
        msg = f"[INFO] Updated the version code {version_code_obj.version_code} in database successfully for {filename} " \
            f"for version [{ver_str}] source [{tool.download_url}]"
        logger.info(msg)
        self.messages.append(msg)
        return True

    def get_latest_from_google(self, tool, app):      # noqa: C901
        """
            Download the latest APK from Google Play Store

            Args,
            tool: Version object containing the version info
            app: APK package name

            Returns,
            True if the tool is updated, False otherwise
        """

        if not tool:
            msg = f"[ERROR] [{app}] Tool is not defined"
            logger.error(msg)
            self.messages.append(msg)
            return False

        toolname = tool.tool.name
        if not app:
            msg = f"[ERROR] tool [{toolname}] does not have a package name"
            logger.error(msg)
            self.messages.append(msg)
            return False

        details = None
        try:
            details = self.api.details(app)
        except Exception as error:
            if "not found" in str(error):
                msg = f"[ERROR] {toolname} [{app}] is incompatible with the device [{self.device_name} | ({self.device_codename})]."
                logger.error(msg)
                self.messages.append(msg)
            else:
                msg = f"[ERROR] {toolname} [{app}] retrieving details failed due to: {error}"
                logger.error(msg)
                self.messages.append(msg)
            return False

        doc = details
        app_details = doc.get('details').get('appDetails')

        if not doc:
            msg = f"[ERROR] {toolname} [{app}] Could not find doc"
            logger.error(msg)
            self.messages.append(msg)
            return False

        if len(doc['offer']) == 0:
            msg = f"[ERROR] {toolname} [{app}] The offer type does not exist"
            logger.error(details)
            logger.error(msg)
            logger.error(f'[ERROR] {str(doc)}')
            self.messages.append(msg)
            self.logged_in = False
            return False

        ver_str = app_details.get('versionString', None)
        ver_code = app_details.get('versionCode', None)
        offer = doc['offer'][0]['offerType']
        size = app_details.get('installationSize', None)
        upload_date = app_details.get('uploadDate', None)
        permission_list = app_details.get('permission', None)

        if not ver_str:
            msg = f"[ERROR] {toolname} [{app}] Unable to find the latest version string"
            logger.error(msg)
            self.messages.append(msg)
            return False

        if ver_code == 0 or not ver_code:
            msg = f"[ERROR] {toolname} [{app}] Unable to find the latest version code"
            logger.error(msg)
            self.messages.append(msg)
            return False

        # Getting app data from google
        try:
            app_data = self.api.delivery(app, ver_code, offer)
        except Exception as e:
            msg = f"[ERROR] {toolname} [{app}] Unable to download app due to: [{e}]"
            logger.error(msg)
            self.messages.append(msg)
            return False

        logger.info("----------------APP DATA----------------")
        logger.info(app_data)

        rel_date = datetime.now()
        if upload_date:
            try:
                rel_date = datetime.strptime(
                    app_details['uploadDate'], '%b %d, %Y')
            except Exception as e:
                msg = f"[ERROR] [{str(app)}] Date [{upload_date}] conversion error [{e}]"
                logger.error(msg)
                self.messages.append(msg)

        tz = 'Iran'
        try:
            rel_date = pytz.timezone(tz).localize(rel_date, is_dst=None)
        except pytz.exceptions.NonExistentTimeError:
            rel_date = pytz.timezone(tz).localize(rel_date)
            msg = f"[ERROR] NonExistentTimeError: [{str(app)}] Date [{upload_date}] localization error"
            logger.error(msg)
            self.messages.append(msg)
        except pytz.exceptions.AmbiguousTimeError:
            rel_date = pytz.timezone(tz).localize(rel_date)
            msg = f"[ERROR] AmbiguousTimeError: [{str(app)}] Date [{upload_date}] localization error"
            logger.error(msg)
            self.messages.append(msg)

        # Check for version string/name, if not same with the existing one, create a new Version object and delete previous one
        # To keep only one version in the system
        # updating version name in existing one and delete versionCode objects related to it
        if tool.version_number != ver_str:
            msg = f"[INFO] Updating version for {tool} to Version ({ver_str})..."
            logger.info(msg)
            # deleting VersionCode objects related to existing Version(tool) object and setting new version name
            msg = f"[INFO] Deleting version code objects for {tool} | Version ({tool.version_number}) ..."
            logger.info(msg)
            VersionCode.objects.filter(version=tool).delete()
            tool.version_number = ver_str
            tool.release_date = rel_date
            tool.last_modified = rel_date
            tool.save()

        # create a VersionCode if not found for given versionName and ver_code
        version_code_obj, vc_created = VersionCode.objects.get_or_create(
            version=tool,
            version_code=ver_code
        )

        # adding device to the version code object
        logger.info(f"Adding the current device [{self.device_codename}] to the devices of version code [{version_code_obj.version_code}]...")
        try:
            version_code_obj.devices.add(
                AndroidDeviceProfile.objects.get(codename=self.device_codename))
            version_code_obj.save()
        except Exception as e:
            logger.error(f"Unable to add the current device to the devices of the version code [{version_code_obj.version_code}] due to:\n{e}")

        # If versionCode is created, download and update file to uploaded_file
        # If versionCode obj already exists, continue to check for splits if the app/tool is bundled app
        if not vc_created:
            msg = f"[INFO] {toolname} [{app}] is up-to-date (version: {ver_str}) | (version code: {ver_code})"
            logger.info(msg)
            self.messages.append(msg)

            extension = version_code_obj.uploaded_file.name.split(
                '.')[-1].lower()

            if tool.is_bundled_app is True and extension == 'apk':
                logger.info(f"{tool} is marked as a bundled app but with no bundled release binary (zip file) yet! "
                            f"Checking if there are more distinct splits for the app on Google Play Store...")
            else:
                return False

        permissions = None
        if permission_list:
            permissions = ', '.join(permission_list)

        # Create/update split files, if any
        splits = app_data.get('splits')
        if splits:
            logger.info(f"Splits were found for [{toolname}] as part of the returned PlayStore app_data!")

            if tool.is_bundled_app is False:
                tool.is_bundled_app = True
                tool.save()
                logger.info(f"Note: The {toolname} version has been marked as a bundled app (supports split APKs.)")

            for split in splits:
                split_type = split.get('name').split('.')[-1]
                split_size = int(split.get('file').get('total_size'))

                # Include split size in ABI split names to create a distinct ABI split
                # only when there is a new ABI variation with a different size
                if split_type in ABI_SPLIT_TYPES:
                    splitname = 'split_config.' + split_type + \
                        '.' + str(split_size) + '.apk'
                else:
                    splitname = 'split_config.' + split_type + '.apk'

                split_path = f"{TOOLS_PATH}{tool.tool.get_app_name()}/{settings.ANDROID_PREFIX}{version_code_obj.version_code}/{SPLITS_PATH}{splitname}"
                split_data = split.get('file').get('data')

                try:
                    splitfile, created = AndroidSplitFile.objects.get_or_create(
                        version=tool,
                        split_file=split_path,
                        size=split_size,
                        tool_version_code=version_code_obj)
                except Exception as e:
                    logger.error(f"[ERROR] Getting or creating the split file [{split_path}] has failed due to:\n{e}")
                    break

                current_split_size = self.convert_size(int(splitfile.size))

                if created:
                    split_temp = self.write_temp_file_to_memory(
                        data=split_data, max_size=50000000)
                    logger.info(f"Split temp file created in memory: {split_temp}")

                    splitfile.split_file.save(
                        split_path, File(split_temp), save=False)
                    splitfile.split_file.name = split_path

                    logger.info(f"A new SplitFile object has been created with the name: [{splitname}] "
                                f"(path: [{split_path}] | size: [{current_split_size}]) ")
                # if the split already exists
                elif splitfile.split_file.storage.exists(splitfile.split_file.name):
                    logger.info(f"A split file with the name [{splitname}] ({current_split_size}) already exists.")
                else:
                    logger.error(f"Unable to create or get splitFile [{split_path}]")
                    break

                logger.info(f"Adding the current device [{self.device_codename}] to the devices of split file [{split_path}]...")
                try:
                    splitfile.devices.add(AndroidDeviceProfile.objects.get(
                        codename=self.device_codename))
                except Exception as e:
                    logger.error(f"Unable to add the current device to the devices of the split file at [{split_path}] due to:\n{e}")

                if created:
                    msg = f"\t[INFO] [SPLIT] [{splitfile}] has been successfully created in the database " \
                        f"for [{self.device_codename} ({self.device_name})] from source: ['Google Play Store']"
                    logger.info(msg)
                    self.messages.append(msg)
                else:
                    msg = f"\t[INFO] [SPLIT] The split file [{split_path}] is up-to-date."
                    logger.info(msg)
                    self.messages.append(msg)
        else:
            logger.info(f"No splits were found for [{toolname}] on [{self.device_name}] as part of the returned PlayStore app_data!")

        # checking if the tool is not bundled app and version code obj is created, then update the base file into version code object
        if not vc_created and tool.is_bundled_app:
            msg = f"\t[INFO] [BASE] The base APK of {toolname} [{app}] is up-to-date."
            logger.info(msg)
            self.messages.append(msg)
        else:
            logger.warning(f"{toolname} [{app}] new version code {version_code_obj.version_code} downloaded...")
            logger.warning(f"{toolname} [{app}] updating base file into version code {version_code_obj.version_code}...")

            base_data = app_data.get('file').get('data')
            base_temp = self.write_temp_file_to_memory(
                data=base_data, max_size=100000000)

            logger.info(f"Base temp file created in memory: {base_temp}")

            new_size = self.convert_size(int(size))

            tool.permissions = permissions
            tool.last_modified = rel_date
            tool.save()

            # updating version code object
            filename = TOOLS_PATH + f"{tool.tool.get_app_name()}/{settings.ANDROID_PREFIX}{version_code_obj.version_code}/{tool.tool.get_app_name()}-android.apk"
            version_code_obj.uploaded_file.name = filename
            version_code_obj.size = size

            # This save will calculate the PGP signature and checksum, based on the uploaded_file,
            # for unbundled apps only. Bundeld apps (zipped) will have their signautres and checksums
            # calculated in the bundling (zipping) stage
            version_code_obj.uploaded_file.save(
                filename, File(base_temp), save=True)

            msg = f"[INFO] Updated the version [{tool.version_number}] in database successfully for [{filename}] " \
                f"for version code [{version_code_obj.version_code}] size ({new_size}) " \
                f"source ['Google Play Store']"

            logger.info(msg)
            self.messages.append(msg)
        return True

    def get_latest_version_bulk(self, app_list):
        """
            Download latest version information in bulk

            Args,
            app_list: a list of the package_names to be downloaded
        """

        if len(app_list) == 0:
            return False

        details = self.api.bulkDetails(app_list)
        for d in details.entry:
            doc = d.doc
            app_details = doc['details']['appDetails']
            ver_str = app_details.get('versionString', None)
            ver_code = app_details.get('versionCode', None)
            offer_type = doc['offer'][0]['offerType']
            logger.info(doc)
            logger.info(f'\tversionString = {ver_str}')
            logger.info(f'\tversionCode = {ver_code}')
            logger.info(f'\tofferType = {offer_type}')

    def download_tool(self, tool):
        """
            Download a tool either from google or the site

            Args:
            tool: A version instance of the tool to be downloaded

            Returns:
            Name of the app if updated, None otherwise
        """

        toolname = tool.tool.name
        if toolname is None:
            logger.error(f"Tool {tool.id} does not have tool name")
            return None

        pkgname = tool.package_name
        if pkgname is None:
            logger.error(f"Tool {tool.id} does not have package name")
            return None

        logger.info(f"\t\t {toolname} --> {pkgname}")

        if '//play.google.com/' in tool.download_url:
            if self.get_latest_from_google(tool, pkgname):
                return True
            return None
        else:
            try:
                if self.get_latest_from_url(tool):
                    return True
                return False
            except KeyboardInterrupt:
                raise
            except Exception as e:
                msg = f"[ERROR] Unable to download from URL {pkgname}: {e}"
                logger.error(msg)
                self.messages.append(msg)
                self.logged_in = False
                return None
