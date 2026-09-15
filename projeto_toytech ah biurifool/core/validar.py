class Validador:
    @staticmethod
    def required(value, field_name):
        if value is None or str(value).strip() == "":
            return f"O campo {field_name} é obrigatório."
        return None

    @staticmethod
    def non_negative(value, field_name):
        try:
            if float(value) < 0:
                return f"O campo {field_name} não pode ser negativo."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None

    @staticmethod
    def positive(value, field_name):
        try:
            if int(value) <= 0:
                return f"O campo {field_name} deve ser maior que zero."
        except (TypeError, ValueError):
            return f"O campo {field_name} deve ser numérico."
        return None

    @staticmethod
    def count_to_8(value, field_name):
        str_valor = str(value).strip()
        if str_valor != 8 :
            return f"O campo {field_name} é obrigatório que tenha exatamente 8 caracteres"
        return None

    @staticmethod
    def count_to_9(value, field_name):
        str_valor = str(value).strip()
        if str_valor != 9 :
            return f"O campo {field_name} é obrigatório que tenha exatamente 8 caracteres"
        return None

    @staticmethod
    def count_to_11(value, field_name):
        str_valor = str(value).strip()
        if str_valor != 11 :
            return f"O campo {field_name} é obrigatório que tenha exatamente 8 caracteres"
        return None
    
    @staticmethod
    def count_to_14(value, field_name):
        str_valor = str(value).strip()
        if str_valor != 14 :
            return f"O campo {field_name} é obrigatório que tenha exatamente 8 caracteres"
        return None
    
    @staticmethod
    def have_number(value, field_name):
        tem_numero= False
        for caractere in value:
            if caractere.isdigit():
                tem_numero = True
                break
            if not tem_numero:
                tem_numero = False
                return f"O campo {field_name} deve ter caracteres numéricos."
            return None
        return None   
    
    @staticmethod
    def have_scaracter(value, field_name):
        tem_scaracter= False
        for caractere in value:
            if caractere.isalnum():
                tem_scaracter = True
                break
            if not tem_scaracter:
                tem_scaracter = False
                return f"O campo {field_name} deve ter caracteres especiais."
            return None
        return None 
    
    @staticmethod
    def not_have_scaracter(value, field_name):
        tem_scaracter= False
        for caractere in value:
            if not caractere.isalnum():
                tem_scaracter = False
                break
            if tem_scaracter:
                tem_scaracter = True
                return f"O campo {field_name} não deve ter caracteres especiais."
            return None
        return None 

    @staticmethod
    def not_have_number(value, field_name):
        tem_numero= False
        for caractere in value:
            if not caractere.isdigit():
                tem_numero = False
                break
            if tem_numero:
                tem_numero = True
                return f"O campo {field_name} não deve ter caracteres numéricos."
            return None
        return None

    
    @staticmethod
    def have_upper(value, field_name):
        tem_maiuscula= False
        for caractere in value:
            if caractere.isupper():
                tem_maiuscula = True
                break
            if not tem_maiuscula:
                tem_maiuscula = False
                return f"O campo {field_name} deve ter letras maiúsculas"
            return None
        return None
    
    @staticmethod
    def not_have_upper(value, field_name):
        tem_maiuscula= False
        for caractere in value:
            if not caractere.isupper():
                tem_maiuscula = False
                break
            if tem_maiuscula:
                tem_maiuscula = True
                return f"O campo {field_name} não deve ter letras maiúsculas"
            return None
        return None