from tokenize import endpats


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    try:
        f = open(file_path, 'r', encoding='utf-8')
    except FileNotFoundError:
        return None

    f.readline()
    anni = []
    for line in f:
        parola = line.strip().split(',')
        if len(parola) >= 5:
            d = {
                'codice': parola[0],
                'titolo': parola[1],
                'autore': parola[2],
                'mese': int(parola[3]),
                'anno': int(parola[4])
            };
        if d['anno'] not in anni:
            anni.append(d['anno'])
    f.close()
    return anni


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    if mese < 1 or mese > 12:
        return None

    for lista_foto in album.values():
        for foto in lista_foto:
            if foto['codice'] == codice:
                return None

    nuova_foto = {
        'codice':codice,
        'titolo': titolo,
        'autore': autore,
        'mese':mese,
        'anno':anno
    }
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"\n{codice}, {titolo}, {autore}, {mese}, {anno}")
    except FileNotFoundError:
        return None

    if anno not in album:
        album[anno] = []
    album[anno].append(nuova_foto)
    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    for anno, lista_foto in album.items():
        for foto in lista_foto:
            if foto['codice'] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    if anno not in album:
        return None

    titoli = []
    for foto in album[anno]:
        titoli.append(foto['titolo'])
    return sorted(titoli)


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
