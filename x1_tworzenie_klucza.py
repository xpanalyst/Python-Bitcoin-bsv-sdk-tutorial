from bsv import PrivateKey


# Utwórz nowy klucz prywatny
moj_klucz = PrivateKey()


# Wyświetl klucz
print("Mój klucz prywatny (WIF):", moj_klucz.wif())

 
# Wyświetl klucz publiczny
klucz_publiczny = moj_klucz.public_key()
print("Mój klucz publiczny:", klucz_publiczny.hex())


# Sprawdź i wyswietl swoje adresy
adres_testnet = klucz_prywatny.address(network = "testnet")
adres_mainnet = klucz_prywatny.address(network = "mainnet")
print("Adres testnet :", adres_testnet)
print("Adres mainnet :", addres_mainnet) 
