from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class EmployeeAction(ABC):
    """Interface abstrak untuk semua aksi karyawan."""

    @abstractmethod
    def execute(self, nama1=None, nama2=None, jabatan=None):
        pass


class EmployeeStorage:
    """Class untuk menyimpan dan mengelola data karyawan."""

    def __init__(self):
        self.employees = {}

    def tambah_karyawan(self, nama, jabatan):
        self.employees[nama] = jabatan
        logging.info("Karyawan '%s' ditambahkan", nama)

    def ubah_jabatan(self, nama, jabatan_baru):
        if nama in self.employees:
            jabatan_lama = self.employees[nama]
            self.employees[nama] = jabatan_baru
            logging.info(
                "Jabatan '%s' diubah dari '%s' menjadi '%s'",
                nama, jabatan_lama, jabatan_baru
            )
        else:
            logging.warning("Karyawan '%s' tidak ditemukan", nama)

    def tampilkan(self):
        if not self.employees:
            logging.warning("Belum ada data karyawan")
            return
        for nama, jabatan in self.employees.items():
            logging.info("%s - %s", nama, jabatan)


class AddEmployeeAction(EmployeeAction):
    """Aksi menambah karyawan."""

    def __init__(self, storage):
        self.storage = storage

    def execute(self, nama1=None, nama2=None, jabatan=None):
        self.storage.tambah_karyawan(nama1, jabatan)
        logging.info("Data karyawan disimpan ke sistem HR (simulasi)")


class ShowEmployeeAction(EmployeeAction):
    """Aksi menampilkan karyawan."""

    def __init__(self, storage):
        self.storage = storage

    def execute(self, nama1=None, nama2=None, jabatan=None):
        logging.info("Menampilkan seluruh data karyawan")
        self.storage.tampilkan()


class EditEmployeeAction(EmployeeAction):
    """Aksi mengubah jabatan karyawan."""

    def __init__(self, storage):
        self.storage = storage

    def execute(self, nama1=None, nama2=None, jabatan=None):
        self.storage.ubah_jabatan(nama1, jabatan)


class ActionRegistry:
    """Registry aksi karyawan."""

    def __init__(self):
        self._actions = {}

    def register(self, key, factory):
        self._actions[key] = factory

    def get_action(self, key):
        if key not in self._actions:
            raise ValueError("Aksi tidak terdaftar")
        return self._actions[key]()


class HRSystem:
    """Koordinator eksekusi aksi manajemen karyawan."""

    def __init__(self, registry):
        self.registry = registry

    def kelola_karyawan(self, aksi, nama1=None, nama2=None, jabatan=None):
        action = self.registry.get_action(aksi)
        action.execute(nama1, nama2, jabatan)


# =========================
# SIMULASI PENGGUNAAN
# =========================

storage = EmployeeStorage()

registry = ActionRegistry()
registry.register("tambah", lambda: AddEmployeeAction(storage))
registry.register("tampil", lambda: ShowEmployeeAction(storage))
registry.register("edit",   lambda: EditEmployeeAction(storage))

hr = HRSystem(registry)

# Tambah karyawan
hr.kelola_karyawan("tambah", nama1="Jeje", jabatan="Staff IT")
hr.kelola_karyawan("tambah", nama1="Ichsan", jabatan="Admin")

# Edit jabatan (FITUR BARU)
hr.kelola_karyawan("edit", nama1="Jeje", jabatan="Supervisor IT")

# Tampilkan karyawan
hr.kelola_karyawan("tampil")