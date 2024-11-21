from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Log awal untuk memastikan proses MPI dijalankan
print(f"[DEBUG] Proses {rank} dimulai.")

# Validasi jumlah proses MPI
if size < 4:
    if rank == 0:
        print("[ERROR] Program membutuhkan 4 proses MPI. Jalankan dengan: mpiexec -n 4 python tugas5mpi.py")
    exit()

if rank == 0:
    # P0: Membuat array dan mengirim ke P1
    array = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"P0: Mengirim data ke P1: {array}")
    comm.send(array, dest=1)
    print("[DEBUG] P0: Data telah dikirim ke P1.")

elif rank == 1:
    # P1: Menerima array dari P0 dan mengambil bilangan ganjil
    print("[DEBUG] P1: Menunggu data dari P0...")
    array = comm.recv(source=0)
    print(f"P1: Menerima data dari P0: {array}")
    ganjil = [x for x in array if x % 2 != 0]
    print(f"P1: Mengambil bilangan ganjil: {ganjil}")
    comm.send(ganjil, dest=2)
    print("[DEBUG] P1: Data bilangan ganjil telah dikirim ke P2.")

elif rank == 2:
    # P2: Menerima bilangan ganjil dari P1, menghitung kuadratnya, dan mengirim ke P3
    print("[DEBUG] P2: Menunggu data dari P1...")
    ganjil = comm.recv(source=1)
    print(f"P2: Menerima bilangan ganjil dari P1: {ganjil}")
    hasil_kali = [x * x for x in ganjil]
    print(f"P2: Hasil perkalian kuadrat: {hasil_kali}")
    comm.send(hasil_kali, dest=3)
    print("[DEBUG] P2: Data hasil perkalian kuadrat telah dikirim ke P3.")

elif rank == 3:
    # P3: Menerima hasil dari P2 dan menampilkan hasil
    print("[DEBUG] P3: Menunggu data dari P2...")
    hasil_kali = comm.recv(source=2)
    print(f"P3: Menerima hasil perkalian kuadrat dari P2: {hasil_kali}")
    print(f"P3: Hasil akhir array: {hasil_kali}")
    print("[DEBUG] P3: Data telah diterima dan ditampilkan.")

# Log akhir untuk memastikan proses selesai
print(f"[DEBUG] Proses {rank} selesai.")
