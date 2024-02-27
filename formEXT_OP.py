from mesh.mesh import MeshGeneration
filename = 'C:/Users/joaoc/OneDrive/Documentos/Puc rio - dissertação/Femep_Nurbs/Femep 97.0/models/Dissertation/CircleRefinement2_planeStress'
with open(f'{filename}_planeStress2.txt', 'w') as file:
    knotVectorU = [0.0, 0.0, 0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.0, 1.0]
    knotVectorV = [0.0, 0.0, 0.0, 0.25, 0.5, 0.75, 1.0, 1.0, 1.0]
    degreeU = 2
    degreeV = 2
    uniqueKnotVectorU = sorted(set(knotVectorU))
    uniqueKnotVectorV = sorted(set(knotVectorV))
    NelemU = len(uniqueKnotVectorU) - 1
    NelemV = len(uniqueKnotVectorV) - 1
    Nelem = NelemU * NelemV
    CRegularsU = MeshGeneration.extractionOperatorUnivariate(knotVectorU, degreeU)
    CRegularsV = MeshGeneration.extractionOperatorUnivariate(knotVectorV, degreeV)
    CRegularsBivariate = MeshGeneration.extractionOperatorBivariate(CRegularsV, CRegularsU)
    for j in range(Nelem):
        op = CRegularsBivariate[j].tolist()
        op = str(op).replace('],', '\n').replace('[', '').replace(']', '').replace(',', '')
        file.write(f"{op}\n\n")