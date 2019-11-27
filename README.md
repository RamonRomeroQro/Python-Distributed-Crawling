# Distributed WebScrapping

```

Copyright 2019 
© Ramon Romero   @RamonRomeroQro

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

```

## SetUp

+ Descargar desde páginas Oficiales: 
   - Python3
   - MongoDB


+ Crear ambiente virtual
```
$ python3 -m venv venv
```
+ Activate venv
```
$ source venv/bin/activate
```
+ install requirements
```
$ pip install -r requirements.txt
```

- Master Node : src/crawler/master.py
- Instancia Esclavo : src/crawler/slave.py [name]
- Parametros : src/settings.json
- database : src/db/init.sh

## Demo

[![DEMO](http://img.youtube.com/vi/DuDJwQcMdAw/0.jpg)](http://www.youtube.com/watch?v=DuDJwQcMdAw)

## Servicios de prueba

- service : test/src/init.py [PORT]
- generate : test/src/generate.py [PORT]

Dataset retrived from:

https://www.kaggle.com/ikarus777/best-artworks-of-all-time



