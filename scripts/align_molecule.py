from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign


ligands = [lig.strip() for lig in open('ligands.dat').readlines()]

align_to = next(Chem.ForwardSDMolSupplier('el.sdf'))

for index, ligand in enumerate(ligands):

    alignee = Chem.MolFromSmiles(ligand)
    alignee = Chem.AddHs(alignee)
    id = AllChem.EmbedMultipleConfs(alignee, numConfs=1)[0]
    AllChem.UFFOptimizeMolecule(alignee, confId=id)

    aligner = rdMolAlign.GetO3A(alignee, align_to)
    aligner.Align()

    Chem.MolToPDBFile(alignee, 'lig-{:02}.pdb'.format(index+1))
