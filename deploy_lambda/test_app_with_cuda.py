import torch

a = torch.rand(1000, 1000).cuda()
b = torch.rand(1000, 1000).cuda()

print(a.shape)
print(b.shape)

c = a.mm(b)
print(c.shape)
