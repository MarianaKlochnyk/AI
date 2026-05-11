import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("Починаємо навчання нейронної мережі...")
model.fit(x_train, y_train, epochs=5)

print("\n--- Оцінка результатів ---")
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'Точність на тестовій вибірці: {test_acc*100:.2f}%')

predictions = model.predict(x_test)
y_pred = np.argmax(predictions, axis=1)
print(f"\nПередбачення моделі для першого тестового зображення: {y_pred[0]}")
print(f"Реальне значення: {y_test[0]}")

error_indices = np.where((y_test == 7) & (y_pred == 1))[0]

if len(error_indices) > 0:
    print(f"\nЗнайдено помилок типу '7 як 1': {len(error_indices)}")
    plt.figure(figsize=(5, 5))
    idx = error_indices[0] 
    plt.imshow(x_test[idx], cmap='gray')
    plt.title(f"Реально: 7 | Мережа каже: 1")
    plt.axis('off')
    plt.show()
else:
    print("\nМодель не переплутала 7 з 1 у цьому тесті.")