import struct
import zlib
BLACK_PIXEL = (0, 0, 0)
WHITE_PIXEL = (255, 255, 255)
HEADER = b'\x89PNG\r\n\x1A\n'
def generate_checkerboard_pattern(width, height):
  out = []
  for i in range(height):
    row = []
    for j in range(width):
      if (i + j) % 2 == 0:
        row.append(WHITE_PIXEL)
      else:
        row.append(BLACK_PIXEL)
    out.append(row)
  return out
def get_checksum(chunk_type, data):
  checksum = zlib.crc32(chunk_type)
  checksum = zlib.crc32(data, checksum)
  return checksum
def chunk(out, chunk_type, data):
  out.write(struct.pack('>I', len(data)))
  out.write(chunk_type)
  out.write(data)
  checksum = get_checksum(chunk_type, data)
  out.write(struct.pack('>I', checksum))
def make_ihdr(width, height, bit_depth, color_type):
  return struct.pack('>2I5B', width, height, bit_depth, color_type, 0, 0, 0)
def encode_data(img):
  ret = []
  for row in img:
    ret.append(0)
    color_values = [
      color_value
      for pixel in row
      for color_value in pixel
    ]
    ret.extend(color_values)
  return ret
def compress_data(data):
  data_bytes = bytearray(data)
  return zlib.compress(data_bytes)
def make_idat(img):
  encoded_data = encode_data(img)
  compressed_data = compress_data(encoded_data)
  return compressed_data
def dump_png(out, img):
  out.write(HEADER)
  assert len(img) > 0  # assume we were not given empty image data
  width = len(img[0])
  height = len(img)
  bit_depth = 8  # bits per pixel
  color_type = 2  # pixel is RGB triple
  ihdr_data = make_ihdr(width, height, bit_depth, color_type)
  chunk(out, b'IHDR', ihdr_data)
  compressed_data = make_idat(img)
  chunk(out, b'IDAT', data=compressed_data)
  chunk(out, b'IEND', data=b'')
def save_png(img, filename):
  with open(filename, 'wb') as out:
    dump_png(out, img)
if __name__ == '__main__':
  width = 10
  height = 10
  img = generate_checkerboard_pattern(width, height)
  save_png(img, 'out.png')