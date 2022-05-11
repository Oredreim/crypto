# Proyecto Crypto ATDM

## Introduccion
El siguiente proyecto muestra un analisis de datos de crypto monedas y de tweets relacionados de las crypto monedas.

## Descripcion
Este repositorio utiliza paginas web como blockchain.com y crypto.com mas los tweets relacionados a estas paginas para mostrar la informaricon de crypto monedas y dar un veredicto sobre que crypto moneda comprar o vender.

## Instalacion

``` bash
git clone https://github.com/Oredreim/crypto
cd crypto
python3 crypto
```

## Uso

``` bash
usage: crypto.py [-h] [-b] [-p] [-un] [-btc] [-eth] [-wbtc] [-bnb] [-btcc] [-mon] [-aav] [-m MONEDA] [-us USUARIO] [-com COMPARAR]

options:
  -h, --help            show this help message and exit
  -b, --blocks          Listar los bloques
  -p, --prices          Listar los charts
  -un, --untransactions
                        Listar las transacciones aun no aprobadas
  -btc, --bitcoin       Informacion de Bitcoin
  -eth, --ethereum      Informacion de Ethereum
  -wbtc, --wrapped      Informacion de Wrapped Bitcoin
  -bnb, --bnb           Informacion de BNB
  -btcc, --bitcoincash  Informacion de Bitcoin Cash
  -mon, --monero        Informacion de Monero
  -aav, --aave          Informacion de Aave
  -m MONEDA, --moneda MONEDA
                        Buscar tweets de la MONEDA ingresada
  -us USUARIO, --usuario USUARIO
                        Buscar tweets del USUARIO ingresado
  -com COMPARAR, --comparar COMPARAR
                        Compara el valor de la divisa con su ultimo valor encontrado
```
