import uuid
import hashlib
from datetime import datetime
from abc import ABC, abstractmethod


# -------------------------------
# Custom Exceptions
# -------------------------------

class StorageLimitExceeded(Exception):
    pass


class FileNotFoundError(Exception):
    pass


class PermissionDenied(Exception):
    pass


# -------------------------------
# Abstract Storage Backend
# -------------------------------

class StorageBackend(ABC):

    @abstractmethod
    def upload(self, filename, content):
        pass

    @abstractmethod
    def download(self, filename):
        pass

    @abstractmethod
    def delete(self, filename):
        pass


# -------------------------------
# Local Storage Implementation
# -------------------------------

class LocalStorage(StorageBackend):

    def __init__(self):
        self.files = {}

    def upload(self, filename, content): # type: ignore
        self.files[filename] = content
        return True

    def download(self, filename):

        if filename not in self.files:
            raise FileNotFoundError(filename)

        return self.files[filename]

    def delete(self, filename):

        if filename not in self.files:
            raise FileNotFoundError(filename)

        del self.files[filename]


# -------------------------------
# Cloud File
# -------------------------------

class CloudFile:

    def __init__(self, filename, content):

        self.file_id = str(uuid.uuid4())[:8]
        self.filename = filename
        self.content = content

        self.size = len(content.encode("utf-8"))

        self.checksum = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        self.uploaded_at = datetime.now()
        self.version = 1

    def update_content(self, new_content):

        self.content = new_content

        self.size = len(
            new_content.encode("utf-8")
        )

        self.checksum = hashlib.sha256(
            new_content.encode("utf-8")
        ).hexdigest()

        self.version += 1


# -------------------------------
# User Account
# -------------------------------

class User:

    def __init__(self, username, storage_limit):

        self.username = username

        self.__storage_limit = storage_limit
        self.__used_storage = 0

        self.files = {}

    @property
    def available_storage(self):
        return self.__storage_limit - self.__used_storage

    def consume_storage(self, size):

        if self.__used_storage + size > self.__storage_limit:
            raise StorageLimitExceeded(
                "Storage quota exceeded!"
            )

        self.__used_storage += size

    def release_storage(self, size):
        self.__used_storage -= size


# -------------------------------
# Permission Manager
# -------------------------------

class PermissionManager:

    def __init__(self):

        self.permissions = {}

    def grant_access(self, file_id, username, role):

        self.permissions[(file_id, username)] = role

    def check_access(self, file_id, username, required_role):

        role = self.permissions.get(
            (file_id, username)
        )

        hierarchy = {
            "viewer": 1,
            "editor": 2,
            "owner": 3
        }

        return (
            role in hierarchy and
            hierarchy[role] >= hierarchy[required_role]
        )


# -------------------------------
# Cloud Storage Manager
# -------------------------------

class CloudStorageManager:

    def __init__(self, backend):

        self.backend = backend
        self.permission_manager = PermissionManager()

    def upload_file(self, user, filename, content):

        cloud_file = CloudFile(filename, content)

        user.consume_storage(cloud_file.size)

        try:

            self.backend.upload(
                cloud_file.file_id,
                content
            )

            user.files[cloud_file.file_id] = cloud_file

            self.permission_manager.grant_access(
                cloud_file.file_id,
                user.username,
                "owner"
            )

            print(
                f"File uploaded: {filename} "
                f"| Version: {cloud_file.version}"
            )

            return cloud_file

        except Exception:
            user.release_storage(cloud_file.size)
            raise

    def download_file(self, user, file_id):

        if file_id not in user.files:
            raise FileNotFoundError(file_id)

        if not self.permission_manager.check_access(
            file_id,
            user.username,
            "viewer"
        ):
            raise PermissionDenied(
                "You don't have permission to download this file."
            )

        return self.backend.download(file_id)

    def update_file(self, user, file_id, new_content):

        if file_id not in user.files:
            raise FileNotFoundError(file_id)

        if not self.permission_manager.check_access(
            file_id,
            user.username,
            "editor"
        ):
            raise PermissionDenied(
                "Editing permission required."
            )

        cloud_file = user.files[file_id]

        old_size = cloud_file.size
        new_size = len(new_content.encode("utf-8"))

        additional_size = new_size - old_size

        if additional_size > 0:
            user.consume_storage(additional_size)

        try:

            self.backend.upload(
                file_id,
                new_content
            )

            cloud_file.update_content(new_content)

            if additional_size < 0:
                user.release_storage(-additional_size)

            print(
                f"File updated successfully. "
                f"New version: {cloud_file.version}"
            )

        except Exception:

            if additional_size > 0:
                user.release_storage(additional_size)

            raise

    def delete_file(self, user, file_id):

        if file_id not in user.files:
            raise FileNotFoundError(file_id)

        cloud_file = user.files[file_id]

        if not self.permission_manager.check_access(
            file_id,
            user.username,
            "owner"
        ):
            raise PermissionDenied("Only owners can delete files.")

        self.backend.delete(file_id)

        user.release_storage(cloud_file.size)

        del user.files[file_id]

        print("File deleted successfully!")


# -------------------------------
# Application Execution
# -------------------------------

backend = LocalStorage()

cloud = CloudStorageManager(backend)

# Create user
user = User(
    username="Rishav",
    storage_limit=10000
)

# Upload file
file = cloud.upload_file(
    user,
    "project.txt",
    "Python OOP Cloud Storage Project"
)

print("\nAvailable Storage:", user.available_storage)

# Download file
print("\nDownloaded Content:")

content = cloud.download_file(
    user,
    file.file_id
)

print(content)

# Update file
print("\nUpdating File...")

cloud.update_file(
    user,
    file.file_id,
    "Updated Python OOP Cloud Storage Project"
)

# Display metadata
print("\n----- File Metadata -----")

print("File ID:", file.file_id)
print("Filename:", file.filename)
print("Version:", file.version)
print("Checksum:", file.checksum)
print("File Size:", file.size)

# Delete file
print("\nDeleting File...")

cloud.delete_file(
    user,
    file.file_id
)

print("Remaining Storage:", user.available_storage)