import torch
f = torch.load('resnext101_32x4d.pth')

if 'state_dict' in f.keys():
    f = f['state_dict']
names = list(f.keys())
for item in names:
    if 'layer' in item:
        f['second_'+item] = f[item]

torch.save(f,'db-resnext101_32x4d.pth')
