# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.

"""
import pandas as pd
import os
import zipfile

def pregunta_01():
    def generar_datasets():
        # Ruta de los archivos
        input_path = "files/input.zip"
        output_path = "files/output"
        extract_folder = "files/input"

        # Descomprimir el archivo ZIP si no ha sido descomprimido previamente
        if not os.path.exists(extract_folder):
            print("Descomprimiendo archivo ZIP...")
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                zip_ref.extractall("files")

        # Crear la carpeta de salida si no existe
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Verificar la estructura de carpetas después de descomprimir
        print("Verificando la estructura de directorios descomprimidos...")
        for root, dirs, files in os.walk(extract_folder):
            print(f"Directorio: {root}, Subdirectorios: {dirs}, Archivos: {files}")

        # Función para crear el dataset a partir de un directorio de entrada
        def crear_dataset(directorio):
            data = []
            for sentiment in ["negative", "positive", "neutral"]:
                sentiment_folder = os.path.join(directorio, sentiment)
                if not os.path.exists(sentiment_folder):
                    print(f"Advertencia: No se encontró la carpeta {sentiment_folder}")
                    continue
                for filename in os.listdir(sentiment_folder):
                    if filename.endswith(".txt"):
                        filepath = os.path.join(sentiment_folder, filename)
                        with open(filepath, 'r', encoding="utf-8") as f:
                            phrase = f.read().strip()
                        data.append({"phrase": phrase, "target": sentiment})
            return data

        # Crear datasets para 'train' y 'test'
        print("Generando dataset para 'train'...")
        train_data = crear_dataset(os.path.join(extract_folder, "train"))
        print(f"Se generaron {len(train_data)} registros para 'train'.")

        print("Generando dataset para 'test'...")
        test_data = crear_dataset(os.path.join(extract_folder, "test"))
        print(f"Se generaron {len(test_data)} registros para 'test'.")

        # Si los datasets están vacíos, se reporta un problema
        if not train_data or not test_data:
            print("Error: No se generaron datos para los datasets.")
            return

        # Convertir las listas de datos en DataFrames
        train_df = pd.DataFrame(train_data)
        test_df = pd.DataFrame(test_data)

        # Verificar que los DataFrames contienen datos
        print(f"Train dataset tiene {len(train_df)} filas.")
        print(f"Test dataset tiene {len(test_df)} filas.")

        # Guardar los datasets como CSV en la carpeta output
        try:
            if not train_df.empty:
                print("Guardando 'train_dataset.csv'...")
                train_df.to_csv(os.path.join(output_path, "train_dataset.csv"), index=False)
                print("Archivo 'train_dataset.csv' guardado correctamente.")
            else:
                print("Advertencia: El dataset de entrenamiento está vacío. No se guardó el archivo 'train_dataset.csv'.")

            if not test_df.empty:
                print("Guardando 'test_dataset.csv'...")
                test_df.to_csv(os.path.join(output_path, "test_dataset.csv"), index=False)
                print("Archivo 'test_dataset.csv' guardado correctamente.")
            else:
                print("Advertencia: El dataset de prueba está vacío. No se guardó el archivo 'test_dataset.csv'.")
        
        except Exception as e:
            print(f"Error al guardar los archivos CSV: {e}")

    # Llamada a la función para generar los datasets
    generar_datasets()

if __name__ == "__main__":
    pregunta_01()


    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
