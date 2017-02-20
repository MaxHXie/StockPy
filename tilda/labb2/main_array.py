from array import array
from arrayQFile import ArrayQ

q = ArrayQ()
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

#input en lista, gör en array, returnera array
def make_array(cards_input_list):
    cards_array = ArrayQ(cards_input_list)
    return cards_array

def main():
    cards_input_list = take_input()
    cards_array = make_array(cards_input_list)
    answerList = []
    while cards_array.isEmpty() == False:
        replaced_card = cards_array.dequeue()
        cards_array.enqueue(replaced_card)

        removed_card = cards_array.dequeue()
        answerList.append(removed_card)

    print()
    print("Simsalabim!")
    for i in range(len(answerList)):
        print(str(answerList[i]), end=" ")
    print()

main()
