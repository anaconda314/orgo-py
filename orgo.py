import rdkit.Chem as chem
Mol = chem.Mol

def hydrogenate(inchi: str):
	m = chem.MolFromInchi(inchi)

	# performs hydrolysis on the Mol in place
	for bond in m.GetBonds():
		if bond.GetBondType() == chem.BondType.DOUBLE:
			bond.SetBondType(chem.BondType.SINGLE)
	return [chem.MolToInchi(m)]

def ozonolyse(inchi: str):
	m = chem.MolFromInchi(inchi)

	#makes a copy of the mol and performs ozonolysis
	em = chem.EditableMol(m)
	em.BeginBatchEdit()
	for bond in m.GetBonds():
		if bond.GetBondType() == chem.BondType.DOUBLE:
			a1 = bond.GetBeginAtomIdx()
			a2 = bond.GetEndAtomIdx()
			em.RemoveBond(a1, a2)

			o1 = em.AddAtom(chem.Atom("O"))
			em.AddBond(a1, o1, chem.BondType.DOUBLE)

			o2 = em.AddAtom(chem.Atom("O"))
			em.AddBond(a2, o2, chem.BondType.DOUBLE)
	em.CommitBatchEdit()

	m = em.GetMol()
	m_list = chem.GetMolFrags(m, asMols=True, sanitizeFrags=True)
	return [ chem.MolToInchi(mol) for mol in m_list ]


'''
def halogenate(m: Mol, halogen: str):
	# makes a copy of the mol and performs bromination
	for bond in m.GetBonds():
		if bond.GetBondType() == chem.BondType.DOUBLE:
			em = chem.EditableMol(m)
			em.BeginBatchEdit()

			a1 = bond.GetBeginAtomIdx()
			a2 = bond.GetEndAtomIdx()
			em.RemoveBond(a1, a2)

			br1 = em.AddAtom(chem.Atom(halogen))
			bond1 = em.AddBond(a1, br1, chem.BondType.SINGLE)

			br2 = em.AddAtom(chem.Atom(halogen))
			bond2 = em.AddBond(a2, br2, chem.BondType.SINGLE)

			em.CommitBatchEdit()
			# removes double bond, bonding the atoms to new
			#  halogen atoms


			m = em.GetMol()
			m.GetBondWithIdx(bond1).SetBondDir(chem.BondDir.BEGINWEDGE)
			m.GetBondWithIdx(bond2).SetBondDir(chem.BondDir.BEGINDASH)
			# makes the two new bonds go in opposite directions
	return m
'''
