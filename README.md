aesQR
=====

simple bit of *POC* python code for storing a AES key or encrypted AES data in a QR code.

Example QR code
---------------
### encodeKey
`test_key = "f4eba54dab7b4cdcb34f13689beea128acdc8960c8ec4c929d0c9f85d2fa5c22"`

![Example QR code image containing AES key](code.png)

### encodeAES
`test_key = "c8a8cfbe019242bdb8d376a881ce77f09f05c4f31e2444bf8dbc87261c2c0397"`

`plaintext = "weeeeeeeeeeeeeeeeeeeeeeeeeeeeee, we like to encrypt aes data in qr codes"`

![Example QR code image containing encrypted AES data](code2.png)

Requirements
------------
* `qrtools` (`python-qrtools` package on ubuntu)
* `dAES` (This is a library I wrote, [here](https://github.com/rolandshoemaker/d-AES), that uses dynamic s-boxes but any AES library could be used!)
