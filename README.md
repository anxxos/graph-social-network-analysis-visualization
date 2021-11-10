# Práctica Final de Análisis de Grafos y RRSS
## Muestra de Red de Relaciones SWIFT

###### Abril 2019

> Para un correcto funcionamiento, utilizar **PyCharm** y abrir el repositorio como proyecto. Ejecutar entonces el archivo HTML y visualizar en Google Chrome. En la carpeta _images_ podrás ver una muestra del resultado de la ejecución del proyecto.

En este repositorio encontrarás los datos en formato CSV ya tokenizados y 'parseados', el análisis de los datos con el archivo JSON final, y la visualización de los mismos. 
No se adjuntan los datos originales por motivos de  seguridad. No obstante, se relatará brevemente su obtención en el siguiente apartado.

### Obtención y tokenización
Se han leído los archivos en formato PARQUET necesarios. Posteriormente, se ha efectuado una reducción considerable de los mismos, restando únicamente una pequeña muestra de mensajes SWIFT de categoría MT103 y una selección de variables de mayor interés. Además, se han 'parseado' los campos que contienen los datos de los clientes para la obtención de su nombre, pues los archivos parquet vienen tal que: _//cuenta XXXXXXXXX\1 nombre cliente\dirección_ o _/cuenta XXXXXXXXXXX\nombre cliente_, etc.

Posteriormente, los datos se han anonimizado y se ha realizado un subset de los mismos con algunos clientes en concreto para aportar más valor desde el punto de vista de negocio. El dataset subset adjunto se denomina tokenized_df.csv.

### Análisis
Se adjunta también el archivo analysis.py donde se ha realizado la transformación del dataset para que pueda ser cargado en un grafo. Los mensajes van desde un cliente deudor, pasando por un banco emisor, a un banco receptor, y por último a un cliente beneficiario; por lo que la generación de todos estos enlaces es necesaria en la transformación.

Por otro lado, se han aplicado varios **algoritmos** de **obtención de importancia** y **centralidad de nodos**, así como de **enlaces**, y de **detección de comunidades**.

### Visualización
Se realiza mediante el código HTML adjunto. La visualización de la red contiene diversas funcionalidades: movimiento de nodos y enlaces, búsqueda de nodos, enlaces y énfasis, tool-tips de atributos de enlaces y nodos, resaltado de nodos y vecinos, aumento del tamaño de nodos, y zoom sobre la red.

La carpeta de visualización contiene un fichero con iconos que se utilizaron para otras versiones de la práctica, pero no relevantes en la versión final.
