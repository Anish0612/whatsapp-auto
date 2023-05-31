# whatsapp

WhatsApp Web Automation Library using selenium.

# whatsapp

It is a Simple WhatsApp Web Automation Library using selenium.


## Installation

```console
pip install whatsapp-auto
```

whatsapp-auto officially supports Python 3.7+.

## Usage

### Default

```python
import whatsapp_auto

whatsapp = whatsapp_auto.Login()  # Scan the qr code

whatsapp.send_message(phone_no,message) # whatsapp.send_message('+919372091360','hii')

```

### Send File

```python
whatsapp.send_file(phone_no,file_path,caption)  # whatsapp.send_file('+919372091360','/Users/anish/Desktop/whatsapp/Image.png','image')
```

### Send Multiple File

```python
whatsapp.send_multiple_files(phone_no,folder_path,caption)  # whatsapp.send_multiple_files('+919372091360','/Users/anish/Desktop/whatsapp/','image')
```

### Send Message to Group

```python
whatsapp.send_message_to_group(group_link,message)   # whatsapp.send_message_to_group('J6iHb0tR0ky5lJITHLV03b','hi')
```

### Send File to Group

```python
whatsapp.send_file_to_group(group_link,file_path,caption)  # whatsapp.send_file_to_group('J6iHb0tR0ky5lJITHLV03b','/Users/anish/Desktop/image.png')
```

### Send Multiple File to Group

```python
whatsapp.send_multiple_files_to_group(group_link,folder_path,caption) # whatsapp.send_multiple_files_to_group('J6iHb0tR0ky5lJITHLV03b','/Users/anish/Desktop/whatsapp/')
```

### To close browser

```python
whatsapp.close()
```
