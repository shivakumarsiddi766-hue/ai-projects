import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

data = {
    "size":[1000,1500,2000,2500,3000],
    "bedrooms":[2,3,4,4,5],
    "age":[10,5,2,1,1],
    "price":[200000,300000,400000,500000,600000]
}

df = pd.DataFrame(data)


X = df[["size","bedrooms","age"]].values
y = df["price"].values

X = torch.tensor(X,dtype=torch.float32)
y = torch.tensor(y,dtype=torch.float32).view(-1,1)


class HousePriceModel(nn.Module):

    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(3,16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16,8)
        self.fc3 = nn.Linear(8,1)

    def forward(self,x):

        x = self.fc1(x)
        x = self.relu(x)

        x = self.fc2(x)
        x = self.relu(x)

        x = self.fc3(x)

        return x
model = HousePriceModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(500):

    pred = model(X)

    loss = criterion(pred,y)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if epoch % 50 == 0:
        print("Epoch:",epoch,"Loss:",loss.item())

test = torch.tensor([[2200,4,3]],dtype=torch.float32)

predicted_price = model(test)

print(predicted_price)