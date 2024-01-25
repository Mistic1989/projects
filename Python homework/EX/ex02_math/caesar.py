"""Caesar cipher."""

from string import ascii_lowercase


def encode(message: str, shift: int) -> str:
    """
    Encode a message using a Caesar cipher.

    Presume the message is already lowercase.
    For each letter of the message, shift it forward in the alphabet by shift amount.
    If the character isn't a letter, keep it the same.

    For example, shift = 3 then a => d, b => e, z => c (see explanation below)

    Shift:    0 1 2 3
    Alphabet:       A B C D E F G H I J
    Result:   A B C D E F G H I J

    Examples:
    1. encode('i like turtles', 6) == 'o roqk zaxzrky'
    2. encode('example', 1) == 'fybnqmf'
    3. encode('the quick brown fox jumps over the lazy dog.', 7) == 'aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.'

    :param message: message to be encoded
    :param shift: shift for encoding
    :return: encoded message
    """
    alphabet = ascii_lowercase
    encoded_message = ""

    for letter_index in range(len(message)):
        # Check whether the string (message) consists of alphabetic characters only.
        if message[letter_index].isalpha():
            alphabet_index = 0
            # Loop through alphabet.
            while alphabet_index < len(alphabet):
                # When letter in message matches letter in alphabet.
                if message[letter_index] == alphabet[alphabet_index]:
                    # Check if the new position is greater than the length of the alphabet.
                    if alphabet_index + shift > len(alphabet) - 1:  # len(alphabet) is 26
                        # Calculate new position because new position is greater than the length of the alphabet.
                        alphabet_index = (alphabet_index + shift) % len(alphabet)
                        # Add new position of the letter to a variable
                        encoded_message += alphabet[alphabet_index]
                        break
                    else:
                        """
                        If the new position is not greater than the length of the alphabet,
                        add new position of the letter to a variable
                        """
                        encoded_message += alphabet[alphabet_index + shift]
                        break
                else:
                    """
                    If the letter in the message doesn't match with the letter in alphabet,
                    move to the next letter in the alphabet.
                    """
                    alphabet_index += 1
        else:
            """
            If letter in the message is not alphabetic character,
            add it to the variable without changing its position.
            """
            encoded_message += message[letter_index]

    return encoded_message


if __name__ == '__main__':
    print(encode("i like turtles", 6))  # -> o roqk zaxzrky
    print(encode("o roqk zaxzrky", 20))  # -> i like turtles
    print(encode("example", 1))  # -> fybnqmf
    print(encode("don't change", 0))  # -> don't change
    print(encode('the quick brown fox jumps over the lazy dog.', 7))  # -> aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.
