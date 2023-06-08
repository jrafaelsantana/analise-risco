import torch.nn as nn

# class NeuralNet(nn.Module):
#   def __init__(self, num_features):
#     super(NeuralNet, self).__init__()
#     self.fc1 = nn.Linear(num_features, 64)
#     self.fc2 = nn.Linear(64, 32)
#     self.fc3 = nn.Linear(32, 1)
#     self.relu = nn.ReLU()
#     self.sigmoid = nn.Sigmoid()

#   def forward(self, x):
#     x = self.relu(self.fc1(x))
#     x = self.relu(self.fc2(x))
#     x = self.sigmoid(self.fc3(x))
#     return x

class NeuralNet(nn.Module):
    def __init__(self, num_features):
        super(NeuralNet, self).__init__()
        self.fc = nn.Linear(num_features, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        output = self.fc(x)
        output = self.sigmoid(output)
        return output