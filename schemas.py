from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum


# ============ ENUMS ============

class RoleEnum(str, Enum):
    agent = "agent"
    admin = "admin"


class ModePaiementEnum(str, Enum):
    carte = "carte"
    espece = "espece"
    application = "application"


class EtatVoitureEnum(str, Enum):
    parfait = "parfait"
    nettoyage_requis = "nettoyage_requis"
    dommages_mineurs = "dommages_mineurs"
    dommages_majeurs = "dommages_majeurs"


class StatusVehiculeEnum(str, Enum):
    disponible = "disponible"
    loue = "loue"
    maintenance = "maintenance"


# ============ UTILISATEUR ============

class UtilisateurCreate(BaseModel):
    id_user: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=100)
    prenom: str = Field(..., max_length=100)
    mot_de_passe: str
    role: RoleEnum
    id_admin: Optional[str] = Field(None, max_length=50)


class UtilisateurResponse(BaseModel):
    id_user: str
    nom: str 
    prenom: str
    role: RoleEnum
    id_admin: Optional[str] 

    class Config:
        orm_mode = True

# ============ CLIENT ============

class ClientCreate(BaseModel):
    id_client: str = Field(..., max_length=50)
    nom: str = Field(..., max_length=100)
    prenom: str = Field(..., max_length=100)
    mot_de_passe: str
    adresse: str
    tel: str = Field(..., max_length=20)
    cin: str = Field(..., max_length=20)
    num_permis: str = Field(..., max_length=50)

class ClientResponse(BaseModel):
    id_client :str
    nom : str
    prenom : str
    adresse : str
    tel : str
    cin : str
    num_permis : str

    class Config:
        orm_mode = True
    

# ============ VEHICULE ============

class VehiculeCreate(BaseModel):
    id_vehicule: str = Field(..., max_length=50)
    marque: str = Field(..., max_length=50)
    modele: str = Field(..., max_length=50)
    carburant: str = Field(..., max_length=30)
    prix_par_jour: float = Field(..., gt=0)
    status: str | Optional[StatusVehiculeEnum] = "disponible"

# ============ RESERVATION ============

class ReservationCreate(BaseModel):
    id_reservation: str = Field(..., max_length=50)
    date_debut: date
    date_fin: date
    date_reservation: Optional[date] = None
    montant_total: float = Field(..., ge=0)
    id_client: str = Field(..., max_length=50)
    id_vehicule: str = Field(..., max_length=50)
    id_user: str = Field(..., max_length=50)

# ============ PAIEMENT ============

class PaiementCreate(BaseModel):
    id_paiement: str = Field(..., max_length=50)
    mode_paiement: Optional[ModePaiementEnum] = ModePaiementEnum.carte
    id_reservation: str = Field(..., max_length=50)

# ============ RETOUR ============

class RetourCreate(BaseModel):
    id_retour: str = Field(..., max_length=50)
    date_retour: date
    etat_voiture: EtatVoitureEnum
    frais_supplementaire: Optional[float] = Field(0, ge=0)
    id_reservation: str = Field(..., max_length=50)