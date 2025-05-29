import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA

# Configuração de semente para reprodutibilidade
np.random.seed(42)

# Simulação de dados de pH para 100 dias
ph_base = np.random.uniform(6, 8, 100)
dias = np.arange(1, 101).reshape(-1, 1)

# Selecionar 10 dias aleatórios para simular falhas do sensor
falhas = np.random.choice(dias.flatten(), 10, replace=False)
falhas.sort()

# Perfis de aceitação humana
def human_accepts_conservative(pred):
    return 6.8 <= pred <= 7.2

def human_accepts_flexible(pred):
    return 6.4 <= pred <= 7.6

# Normalização dos dados
scaler_x = StandardScaler()
scaler_y = StandardScaler()
dias_scaled = scaler_x.fit_transform(dias)
ph_scaled = scaler_y.fit_transform(ph_base.reshape(-1, 1)).ravel()

# Modelo de Rede Neural
model_nn = MLPRegressor(hidden_layer_sizes=(10, 10), activation='relu', solver='adam', max_iter=5000, random_state=42)
model_nn.fit(dias_scaled, ph_scaled)
dias_falha_scaled = scaler_x.transform(falhas.reshape(-1, 1))
nn_preds_scaled = model_nn.predict(dias_falha_scaled)
nn_preds = scaler_y.inverse_transform(nn_preds_scaled.reshape(-1, 1)).flatten()

# Modelo ARIMA
model_arima = ARIMA(ph_base, order=(5, 1, 0))
model_fit_arima = model_arima.fit()
arima_preds = model_fit_arima.forecast(steps=10)

# Avaliação de aceitação
acc_cons = []
acc_flex = []

for nn_pred, arima_pred in zip(nn_preds, arima_preds):
    acc_cons.append((human_accepts_conservative(nn_pred), human_accepts_conservative(arima_pred)))
    acc_flex.append((human_accepts_flexible(nn_pred), human_accepts_flexible(arima_pred)))

# Cálculo das taxas
rate_c_nn = sum(1 for a in acc_cons if a[0]) / len(acc_cons)
rate_c_arima = sum(1 for a in acc_cons if a[1]) / len(acc_cons)
rate_f_nn = sum(1 for a in acc_flex if a[0]) / len(acc_flex)
rate_f_arima = sum(1 for a in acc_flex if a[1]) / len(acc_flex)

# Impressão das taxas
print(f"Taxa de aceitação (Conservador) - NN: {rate_c_nn:.2%}, ARIMA: {rate_c_arima:.2%}")
print(f"Taxa de aceitação (Flexível) - NN: {rate_f_nn:.2%}, ARIMA: {rate_f_arima:.2%}")

# Gráfico para Rede Neural
plt.figure(figsize=(10, 5))
plt.scatter(dias, ph_base, color='black', label='Real pH', marker='o')
plt.scatter(falhas, nn_preds, color='green', label='Predictions (NN)', marker='o')

plt.xlabel('Days')
plt.ylabel('pH')
plt.title('pH Prediction using Neural Network')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico para ARIMA
plt.figure(figsize=(10, 5))
plt.scatter(dias, ph_base, color='black', label='Real pH', marker='o')
plt.scatter(falhas, arima_preds, color='blue', label='Predictions (ARIMA)', marker='o')

plt.xlabel('Days')
plt.ylabel('pH')
plt.title('pH Prediction using ARIMA')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
