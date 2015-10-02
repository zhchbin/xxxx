def decode(value, key):
    length_of_value = len(value)
    if length_of_value % 2 == 0:
        mid = length_of_value / 2
        # Split value in the middle -> reverse -> concatenate
        value = value[:mid][::-1] + value[mid:][::-1]
    k = 0
    result = ''
    for v in value:
        c = ord(v)
        bl_1 = 1 if c ^ ord(key[k]) < 32 else 0
        bl_2 = 1 if c ^ ord(key[k]) > 126 else 0
        bl_3 = (1 if c < 0 else 0) | (bl_1 | bl_2)
        bl_4 = (1 if c > 255 else 0) | bl_3
        if bl_4:
            result += v
        else:
            result += chr(c ^ ord(key[k]))
        k = 0 if k + 1 == len(key) else k + 1
    return result

assert decode('QXvGKD', 'Encrypt01') == '362627'
