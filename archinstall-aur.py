import logging
import archinstall
from archinstall import Installer

__version__ = 0.1


class Plugin:
    TEMPORARY_USER_NAME = "aurinstall"
    DEPENDENCIES = ["git"]
    AUR_HELPER_REPOSITORY = "https://aur.archlinux.org/paru-bin.git"

    def on_install(self, installer: Installer):
        packages = archinstall.arguments['packages_aur']
        if len(packages) > 0:
            self.install_dependencies(installer)
            self.create_temporary_user(installer)
            self.enable_passwordless_sudo(installer)
            self.install_aur_helper(installer)
            self.install_aur_packages(packages, installer)
            self.disable_passwordless_sudo(installer)
            self.delete_temporary_user(installer)

    def install_dependencies(self, installer: Installer):
        installer.log(
            f"Installing dependencies needed for AUR package installation: {self.DEPENDENCIES}",
            level=logging.INFO
        )
        installer.pacstrap(self.DEPENDENCIES)

    def create_temporary_user(self, installer: Installer):
        installer.log(
            installer.user_create(self.TEMPORARY_USER_NAME),
            level=logging.DEBUG
        )

    def delete_temporary_user(self, installer: Installer):
        installer.log(
            f'Deleting user {self.TEMPORARY_USER_NAME}',
            level=logging.INFO
        )
        installer.log(
            installer.arch_chroot(f"userdel {self.TEMPORARY_USER_NAME}"),
            level=logging.DEBUG
        )

    def enable_passwordless_sudo(self, installer: Installer):
        installer.log(
            "Temporarily enabling passwordless sudo to use makepkg.",
            level=logging.INFO
        )
        installer.log(
            installer.arch_chroot(r"sed -i 's/# \(%wheel ALL=(ALL) NOPASSWD: ALL\)/\1/' /etc/sudoers"),
            level=logging.DEBUG
        )

    def disable_passwordless_sudo(self, installer: Installer):
        installer.log("Disabling passwordless sudo.", level=logging.INFO)
        installer.log(
            installer.arch_chroot(r"sed -i 's/# \(%wheel ALL=(ALL) NOPASSWD: ALL\)/\1/' /etc/sudoers"),
            level=logging.DEBUG
        )

    def install_aur_helper(self, installer: Installer):
        installer.log("Installing paru aur helper.", level=logging.INFO)
        installer.log(
            installer.arch_chroot(
                f"su aurinstall -c 'cd $(mktemp -d) && git clone {self.AUR_HELPER_REPOSITORY} . && makepkg -sim --noconfirm'"
            ),
            level=logging.DEBUG
        )

    def install_aur_packages(self, packages, installer: Installer):
        installer.log(
            f"Installing aur packages: {' '.join(packages)}",
            level=logging.INFO
        )
        installer.log(
            installer.arch_chroot(
                f'su {self.TEMPORARY_USER_NAME} -c "paru -Sy --nosudoloop --needed --noconfirm {" ".join(packages)}"'),
            level=logging.DEBUG
        )
