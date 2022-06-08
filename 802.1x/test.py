import sys
import keyboard
a=[1,2,3,4]
pause = input("Press y to continue or press n to exit: \n")

# print('test')
# if pause == "y":
#     print('you pressed y')

if pause == 'y':
    print('you pressed y')


# while True:
#     try:
#         if keyboard.is_pressed('y'):
#             print("you pressed Y, so printing the list..")
#             print(a)
#             break
#         if keyboard.is_pressed('n'):
#             print("\nyou pressed N, so exiting...")
#             sys.exit(0)
#     except:
#         break