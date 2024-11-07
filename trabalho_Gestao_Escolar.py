import os

class Endereco:

    def __init__(self, rua: str ='', numero: str ='', bairro: str ='' , cidade: str =''):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
    
    def __str__(self) -> str:
        return f'Rua: {self.rua}, nº {self.numero} Bairro: {self.bairro} - {self.cidade}'

class Pessoa:

    def __init__(self, nome:str, cpf:str, genero:str, endereco: Endereco):
        self.nome = nome
        self.cpf = cpf
        self.genero = genero
        self.endereco = endereco

    def __str__(self) -> str:
        return f'Nome: {self.nome}, CPF: {self.cpf}, Gênero: {self.genero}, \nEndereço: {self.endereco}'     

class Aluno(Pessoa):
    def __init__(self, matricula:str, ano_ingresso:int, nome:str, cpf:str, genero:str, endereco: Endereco):
        super().__init__(nome, cpf, genero, endereco)
        self.matricula = matricula
        self.ano_ingresso = ano_ingresso

    def __str__(self) -> str:
        return f'{self.matricula} - ' + super().__str__()

class Professor(Pessoa):
    def __init__(self, codigo:int, formacao:str, nome:str, cpf:str, genero:str, endereco: Endereco):
        super().__init__(nome, cpf, genero, endereco)
        self.codigo = codigo
        self.formacao = formacao

    def __str__(self) -> str:
        return f'{self.codigo} - ' + super().__str__()
    
class Curso:
    def __init__(self, codigo:int, nome:str, carga_horaria:int, qtd_semestres:int, coordenador: Professor):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.qtd_semestres = qtd_semestres
        self.coordenador = coordenador
        self.turmas = []
    
    def __str__(self) -> str:
        return f'{self.codigo} - Curso: {self.nome}, Carga Horária: {self.carga_horaria} horas, Coordenador: {self.coordenador.nome}'
    
    def pesquisarTurma(self, codigoTurma: int):
        for tur in self.turmas:
            if tur.codigo == codigoTurma:
                return tur
        
        print('\nTurma não encontrada!')
    
    def adicionarTurma(self, turma):
        self.turmas.append(turma)
    
    def removerTurma(self, turma):
        if self.turmas.__contains__(turma):
            self.turmas.remove(turma)
            
    def listarTurmas(self):
        if self.turmas == None or len(self.turmas) == 0:
            print(f'\n o curso {self.nome} não possui turmas cadastradas!')
            return
        
        print(f'\n---Lista de Turmas do curso de {self.nome} ----')
        for tur in self.turmas:
            print(tur)
        

class Turma:
    def __init__(self, codigo:int, descricao:str, ano:int, turno:str, curso:Curso):
        self.codigo = codigo
        self.descricao = descricao
        self.ano = ano
        self.turno = turno
        self.curso = curso
        self.alunos:list[Aluno] = []
    
    def __str__(self) -> str:
        return f'{self.codigo} - Turma: {self.descricao}, Ano: {self.ano}, Turno: {self.turno}'
    
    def quantidadeAlunos(self) -> int:
        return len(self.alunos)
    
    def turmaCheia(self) -> bool:
        if self.quantidadeAlunos() > 40:
            return True
        else:
            return False
        
    def matricularAluno(self, al:Aluno):
        if self.turmaCheia():
            print(f'Não é possível matricular alunos na turma {self.descricao} pois, ela já está cheia!')
        else:
            self.alunos.append(al)
    
    def removerAlunoDaTurma(self, al:Aluno):
        if self.alunos.__contains__(al):
            self.alunos.remove(al)
    
    def listarAlunos(self):
        if self.alunos == None or len(self.alunos) == 0:
            print(f'\n a Turma {self.descricao} não possui alunos matriculados!')
            return
        
        print(f'\n---Lista de Alunos matriculados na Turma {self.descricao} ----')
        for al in self.alunos:
            print(al)

alunos: dict[str, Aluno] = {}
professores: dict[int, Professor] = {}
cursos: dict[int, Curso] = {}
turmas: dict[int, Turma] = {}

def cadastrarEndereco():
    rua = input("Digite a rua do endereço: ")
    numero = input("Digite o número do endereço: ")
    bairro = input("Digite o bairro do endereço: ")
    cidade = input("Digite a cidade do endereço: ")
    return Endereco(rua, numero, bairro, cidade)


def cadastrarAluno():
    nome = input("Digite o nome do aluno: ")
    cpf = input("Digite o CPF do aluno: ")
    genero = input("Digite o gênero do aluno: ")
    matricula = input("Digite a matrícula do aluno: ")
    ano_ingresso = int(input("Digite o ano de ingresso do aluno: "))
    endereco = cadastrarEndereco()
    
    #busca a turma que o aluno irá se matricular
    turma = pesquisarTurma()
    if turma == None:
        print('\nFalha ao matricular aluno na turma!')
        return
    
    aluno = Aluno(matricula, ano_ingresso, nome, cpf, genero, endereco)
    
    #Matricular Aluno em uma Turma
    turma.matricularAluno(aluno)
    
    #adicionar aluno ao dicionário de alunos
    alunos.update({matricula: aluno})
    print(f"O aluno {nome} foi cadastrado com sucesso!")

def editarAluno():
    aluno = pesquisarAluno()  
    if aluno != None:
        aluno.nome = input("Digite o nome do aluno: ")
        aluno.cpf = input("Digite o CPF do aluno: ")
        aluno.genero = input("Digite o gênero do aluno: ")
        aluno.ano_ingresso = int(input("Digite o ano de ingresso do aluno: "))
        op = input("Deseja editar o endereço S/N ? ").upper()
        if(op == 'S'):
            aluno.endereco = cadastrarEndereco()
            
        print("Aluno editado com sucesso!")
    else:
        print("Aluno não encontrado!")

def removerAluno():
    matricula = input("Digite a matrícula do aluno que deseja remover: ")
    if matricula in alunos:
        al = alunos.pop(matricula)
        
        #remover o aluno da turma
        for turma in turmas.values():
            if turma.alunos.__contains__(al):
                turma.removerAlunoDaTurma(al)
                break
        
        print(f'\nO aluno {al.nome} removido com sucesso!')
    else:
        print("\nAluno não encontrado!")

def pesquisarAluno() -> Aluno:
    matricula = input("Digite a matrícula do aluno que deseja pesquisar: ")
    if matricula in alunos:
        al = alunos[matricula]
        print(al)
        return al
    else:
        print("\nAluno não encontrado!")

def cadastrarProfessor():
    codigo = input("Digite o código do professor: ")
    nome = input("Digite o nome do professor: ")
    cpf = input("Digite o CPF do professor: ")
    genero = input("Digite o gênero do professor: ")
    formacao = input("Digite a formação do professor: ")
    endereco = cadastrarEndereco()
    
    professor = Professor(codigo, formacao, nome, cpf, genero, endereco)
    professores.update({codigo:professor})
    print(f'\nO professor {professor.nome} foi cadastrado com sucesso!')

def pesquisarProfessor() -> Professor:
    codigo = input("Digite o código do professor que deseja pesquisar: ")
    if codigo in professores:
        prof = professores[codigo]
        print(prof)
        return prof
    else:
        print("Professor não encontrado!")
        
def editarProfessor():
    prof = pesquisarProfessor()
    if prof != None:     
        prof.nome = input("Digite o novo nome do professor: ")
        prof.cpf = input("Digite o novo CPF do professor: ")
        prof.genero = input("Digite o novo gênero do professor: ")
        prof.formacao = input("Digite a nova formação do professor: ")
        op = input("Deseja editar o endereço S/N ? ").upper()
        if(op == 'S'):
            prof.endereco = cadastrarEndereco()
        print("\nProfessor editado com sucesso!")

def removerProfessor():
    codigo = input("Digite o código do professor que deseja remover: ")
    if codigo in professores:
        prof = professores.pop(codigo)
        print(f"\nO professor {prof.nome} foi removido com sucesso!")
    else:
        print("Professor não encontrado!")
    
def cadastrarCurso():
    coordenador = pesquisarProfessor()
    if coordenador == None:
        print("Coordenador não encontrado. Cadastre o professor antes de continuar.")
        return
    else:
        codigo = int(input("Digite o código do curso: "))
        nome = input("Digite o nome do curso: ")
        carga_horaria = int(input("Digite a carga horária do curso: "))
        qtd_semestres = int(input("Digite a quantidade de semestres do curso: "))
        curso = Curso(codigo, nome, carga_horaria, qtd_semestres, coordenador)
        cursos[codigo] = curso
        print(f"\nO curso {curso.nome} foi cadastrado com sucesso!")

def pesquisarCurso() -> Curso:
    codigo = int(input("Digite o Código do curso que deseja pesquisar: "))
    if codigo in cursos:
        cur = cursos[codigo]
        print(cur)
        return cur
    else:
        print("\nCurso não encontrado!")

def editarCurso():
    cur = pesquisarCurso()
    if cur != None:
        cur.nome = input("Digite o nome do curso: ")
        cur.carga_horaria = int(input("Digite a carga horária do curso: "))
        cur.qtd_semestres = int(input("Digite a quantidade de semestres do curso: "))
        op = input("Deseja alterar o coordenador do curso S/N ? ").upper()
        if(op == 'S'):
            novo_coordenador = pesquisarProfessor()
            if novo_coordenador: 
                cur.coordenador = novo_coordenador
        
        print("\nCurso editado com sucesso!")
    else:
        print("\nCurso não encontrado!")

def removerCurso():
    codigo = input("Digite o Código do curso que deseja remover: ")
    if codigo in cursos:
        cur = cursos.pop(codigo)
        print("\n O curso {cur.nome} foi removido com sucesso!")
    else:
        print("\nCurso não encontrado!")


def cadastrarTurma():
    curso = pesquisarCurso()
    if curso == None:
        print("Curso não encontrado. Cadastre o curso antes de continuar.")
        return
    
    codigo = int(input("Digite o código da turma: "))
    descricao = input("Digite a descrição da turma: ")
    ano = int(input("Digite o ano da turma: "))
    turno = input("Digite o turno da turma (MATUTINO | VESPESTINO | NOTURNO | INTEGRAL): ")

    turma = Turma(codigo, descricao, ano, turno, curso)
    
    #adiciona a turma na lista de turmas do curso
    curso.turmas.append(turma) 
    turmas.update({codigo: turma})
     
    print(f"\n A turma {turma.descricao} foi cadastrada com sucesso!")
    
def pesquisarTurma() -> Turma:
    codigo = int(input("Digite o Código da turma que deseja pesquisar: "))
    if codigo in turmas:
        tur = turmas[codigo]
        print(tur)
        return tur
    else:
        print("Turma não encontrada!")

def editarTurma():
    tur = pesquisarTurma()
    if tur != None:
        tur.descricao = input("Digite a nova descrição da turma: ")
        tur.ano = int(input("Digite o novo ano da turma: "))
        tur.turno = input("Digite o novo turno da turma (manhã/tarde/noite): ")
        
        op = input("Deseja alterar o curso da turma S/N ? ").upper()
        if(op == 'S'):
            novo_curso = pesquisarCurso()
            if novo_curso: 
                #primeiro remove a turma do curso antigo
                tur.curso.removerTurma(tur)
                #atualiza o curso para a turma
                tur.curso = novo_curso
                #adiciona a turma na lista de turmas do novo curso
                novo_curso.adicionarTurma(tur)
                
        print("Turma editada com sucesso!")
    else:
        print("Turma não encontrada!")

def removerTurma():
    codigo = input("Digite o Código da turma que deseja remover: ")
    if codigo in turmas:
        turma = turmas.pop(codigo)
        
        #acessa o curso da turma e remove a turma da lista de turmas do curso
        curso = turma.curso
        curso.removerTurma(turma)
        print(f"\nA turma {turma.descricao} removida com sucesso!")
    else:
        print("Turma não encontrada!")


def listarAlunos():
    print("\n---------Lista de todos os Alunos Cadastrados-------")
    for aluno in alunos.values():
        print(aluno)

def listarAlunosTurma():
    turma = pesquisarTurma()
    if turma:
        turma.listarAlunos()
    
def listarTurmas():
    print("\n---------Lista de todas as Turmas Cadastradas-------")
    for turma in turmas.values():
        print(turma)
        
def listarTurmasCurso():
    curso = pesquisarCurso()
    if curso:
        curso.listarTurmas()

def menuCadastro(classe:str) -> int:
    print(f"\n1 - Inserir {classe}")
    print(f"2 - Editar {classe}")
    print(f"3 - Remover {classe}")
    print(f"4 - Pesquisar {classe}")
    print("0 - Voltar ao menu anterior")
    op = int(input("Digite a opção desejada: "))
    return op
    
def dadosIniciais():
    prof = Professor(10, 'Computaçao', 'João', '99999999', 'M', Endereco())
    cur = Curso(1, 'Informática', 2000, 6, prof)
    tur = Turma(1, 'Primeiro Ano de Informática', 2024, 'MATUTINO', cur )
    
    print(prof)
    print(cur)
    print(tur)
    professores.update({prof.codigo: prof})
    cursos.update({cur.codigo: cur})
    turmas.update({tur.codigo: tur})
    

def menu():
    
    #limpa a tela ao iniciar
    os.system("cls")
    print("\n" * os.get_terminal_size().lines)
    dadosIniciais()
    while True:
        print('\n################################################')
        print('Digite 1 para gerenciar cadastro de Alunos')
        print('Digite 2 para gerenciar cadastro de Professores')
        print('Digite 3 para gerenciar cadastro de Cursos')
        print('Digite 4 para gerenciar cadastro de Turmas')
        print('Digite 5 para listar Alunos')
        print('Digite 6 para listar Turmas')
        print('Digite 0 para sair.\n')
        print('################################################')
        opc = int(input("Digite a opção desejada: "))
        
        if opc == 1:
            while True:
                op = menuCadastro('Aluno')
                if op == 1:
                    cadastrarAluno()
                elif op == 2:
                    editarAluno()
                elif op == 3:
                    removerAluno()
                elif op == 4:
                    pesquisarAluno()
                elif op == 0:
                    break
                else:
                    print("\nOpção inválida!")

        elif opc == 2:
            while True:
                op = menuCadastro('Professor')

                if op == 1:
                    cadastrarProfessor()
                elif op == 2:
                    editarProfessor()
                elif op == 3:
                    removerProfessor()
                elif op == 4:
                    pesquisarProfessor()
                elif op == 0:
                    break
                else:
                    print("\nOpção inválida!")

        elif opc == 3:
            while True:
                op = menuCadastro('Curso')

                if op == 1:
                    cadastrarCurso()
                elif op == 2:
                    editarCurso()
                elif op == 3:
                    removerCurso()
                elif op == 4:
                    pesquisarCurso()
                elif op == 0:
                    break
                else:
                    print("\nOpção inválida!")

        elif opc == 4:
            while True:
                op = menuCadastro('Turma')
                if op == 1:
                    cadastrarTurma()
                if op == 2:
                    editarTurma()
                elif op == 3:
                    removerTurma()
                elif op == 4:
                    pesquisarTurma()
                elif op == 0:
                    break

        elif opc == 5:
            listarAlunosTurma()

        elif opc == 6:
            listarTurmasCurso()

        elif opc == 0:
            break
        else:
            print("Opção inválida!")


menu()