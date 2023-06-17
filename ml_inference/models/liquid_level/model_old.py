import torch.nn as nn

class LiquidLevelNet(nn.Module):
    def __init__(self, num_features):
        super(LiquidLevelNet, self).__init__()
        self.fc = nn.Linear(num_features, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        output = self.fc(x)
        output = self.sigmoid(output)
        return output