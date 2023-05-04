from graphQL.tasks import add

# Call the Celery task asynchronously
print('calling the bg job----------')
add.delay(0, 1)
add.delay(1, 2)
add.delay(3, 1)
add.delay(4, 1)
add.delay(5, 1)
add.delay(6, 1)
add.delay(7, 1)
add.delay(8, 1)
add.delay(9, 1)
add.delay(9, 1)
add.delay(9, 1)
add.delay(9, 1)







