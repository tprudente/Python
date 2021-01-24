v_input = input('introduz um nome: ')
var1 = 'hello'
var2 = 'world'
msg = f'the first {var1} to the {var2} do {v_input}'
print(msg)
print(f'outra maneira de dizer {var1} {var2}')

#unpacking serve para atribuir a variaveis os valores de uma lista por ex
unpacking = ('T','O','m') #lista
a,b,c = unpacking       #a = unpacking[0] etc...
print(F'{a} {b} {c.upper()}')
