class Identifier:
    def validate_identifier(self, identifier):
        valid_id = False
        if identifier:
            achar = identifier[0]
            valid_id = self.valid_s(achar)
        if len(identifier) > 1:
            achar = identifier[1]
            i = 1
            while i < len(identifier) - 1:
                achar = identifier[i]
                if not self.valid_f(achar):
                    valid_id = False
                i = i + 1   # comentar para simular looping infinito

        if valid_id and len(identifier) >= 1 and len(identifier) <= 6:
            return True
        else:
            return False

    def valid_s(self, char):
        if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z'):
            return True
        return False

    def valid_f(self, char):
        if (
                (char >= 'A' and char <= 'Z')
                or (char >= 'a' and char <= 'z')
                or (char >= '0' and char <= '9')
        ):
            return True
        return False