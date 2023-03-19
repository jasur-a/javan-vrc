Componente para subir Archivos, estos se suben a s3 y posteriormente la url devuelta se envía al backend

Funciona como drag and drop y por clicks, se muestran ejemplos de implementación:

### Primero es necesario indicar que este modelo tiene subida de archivos:

En las config del modelo se debe indicar uploadFile en true, de esta manera se hace el llamado de la api de subida de archivos a s3

se hace necesario que las variables que contengan estas url tengan en el nombre "\_url"

```
{
    "alias": ["upload_documentation_operation"],
    "name": "upload_documentation_operation",
    "config":{
    "uploadFile": true
    }
    ....
}
```

### Ejemplo de estructura de modelo:

```
{
    "props": {
    "component": "UploadFile",
    "name": "nif_front_url",
    "label": "Fotografía del DNI",
    "placeholder": "Cara frontal",
    "supported_filetype" : ["jpg", "jpeg", "png"],
    "max_size" = "2000000",
    "validations": {
        "required": true
    },
    "icon": "useAsset(iconDni)"
    },
    "component": "Field"
},
```

### Ejemplo de estructura de style:

```
uploader{
    "container": "color:useColor(primary-red);",
    "button": "font-weight: 500;",
    "label": "text-align: left;"
},
```

### Ejemplo de estructura de configuracion para comprimir imagenes:

```
uploader{
    "compress_quality": 0.7, //se puede enviar tambien desde el model
    "compress_from": 2097152
},
```

compress_quality cadlidad final de la imagen a comprimir ej: 0.7 = 70%
compress_from desde que peso se comenzara a comprimir una imagen ej: 2097152 = 2mb aprox
