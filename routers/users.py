from fastapi import Depends, HTTPException, status, APIRouter
import models
from database import get_db
import schemas
from sqlalchemy.orm import Session
from typing import List
from ..hashing import hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])





#Recupérer tous les utilisateurs
@router.get("/", response_model=List[schemas.UtilisateurResponse])
def get_all_users(db : Session = Depends(get_db)):
    db_agents = db.query(models.Utilisateur).all()
    if  not db_agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucun agent trouvé")
    return db_agents

#Recuperer un utilisateur par id
@router.get("/{id}",response_model=schemas.UtilisateurResponse)
def get_user_by_id(id : str, db : Session = Depends(get_db)):
    got_user = db.query(models.Utilisateur).filter(models.Utilisateur.id_user == id).first()
    if not got_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Utilisateur introuvable")
    return got_user

#Créer un utilisateur 
@router.post("/",response_model=schemas.UtilisateurResponse)
def create_user(request : schemas.UtilisateurCreate,db : Session = Depends(get_db)):
    
    new_user = models.Utilisateur(
        id_user = request.id_user,
        nom = request.nom,
        prenom = request.prenom,
        mot_de_passe = hash_password(request.mot_de_passe),
        role = request.role,
        id_admin = request.id_admin
    )
    if request.role == "agent" :
        admin = db.query(models.Utilisateur).filter(new_user.id_admin == models.Utilisateur.id_admin)
        if not admin :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cet admin n'existe pas")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Supprimer un Utilisateur
@router.delete("/{id_agent}", status_code=status.HTTP_200_OK)
def delete_user(id_agent : str, db : Session = Depends(get_db)):
    deleted_agent = db.query(models.Utilisateur).filter(models.Utilisateur.id_user == id_agent).first()
    if not deleted_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Agent {id_agent} introuvable")
    
    db.delete(deleted_agent)
    db.commit()
    return {"detail": f"{deleted_agent.role} {id_agent} supprimé"}

#Mettre à jour un utilisateur                 
@router.put("/{id_user}")
def update_user(id_user: str, request: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    # 1. Rechercher l'utilisateur existant            
    db_user = db.query(models.Utilisateur).filter(models.Utilisateur.id_user == id_user).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Utilisateur avec l'id {id_user} introuvable"
        )

    update_user = request.model_dump(exclude={"id_user"})
    for key, value in update_user.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user     
