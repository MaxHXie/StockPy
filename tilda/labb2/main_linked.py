from array import array
from linkedQFile import LinkedQ
from linkedQFile import Node

q = LinkedQ()
q.enqueue(1)
q.enqueue(2)
x = q.dequeue()
y = q.dequeue()
print(x,y)

#input inget, tar in ett svar, returnerar en vektor
def take_input():
    cards_input = input("Skriv in kort. Separera med kommatecken (\',\'): ")
    cards_input_list = cards_input.split(",")
    for i in range(len(cards_input_list)):
        cards_input_list[i] = int(cards_input_list[i])

    return cards_input_list

#input en lista, gör en linked list, returnera linked list
def make_Linked(cards_input_list):
    cards_linkedL = LinkedQ()
    for element in cards_input_list:
        cards_linkedL.enqueue(element)
    return cards_linkedL

def main():
    cards_input_list = take_input()
    cards_linkedL = make_Linked(cards_input_list)
    answerList = []
    while cards_linkedL.isEmpty() == False:
        replaced_card = cards_linkedL.dequeue()
        cards_linkedL.enqueue(replaced_card)

        removed_card = cards_linkedL.dequeue()
        answerList.append(removed_card)

    print()
    print("Simsalabim!")
    for i in range(len(answerList)):
        print(str(answerList[i]), end=" ")
    print()

main()
