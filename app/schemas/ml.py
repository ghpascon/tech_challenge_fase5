from pydantic import BaseModel, Field
from typing import Literal


class PredictSchema(BaseModel):
	fase: float = Field(..., description='Feature: fase')
	idade: float = Field(..., ge=0, description='Feature: idade')
	iaa: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador de Auto Avaliação – Média das Notas de Auto Avaliação do Aluno',
	)
	ieg: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador de Engajamento – Média das Notas de Engajamento do Aluno',
	)
	ips: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador Psicossocial – Média das Notas Psicossociais do Aluno',
	)
	ipp: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador Psicopedagógico – Média das Notas Psicopedagógicas do Aluno',
	)
	ida: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador de Aprendizagem – Média das Notas do Indicador de Aprendizagem',
	)
	mat: float = Field(..., ge=0, le=10, description='Nota de Matemática (0–10)')
	por: float = Field(..., ge=0, le=10, description='Nota de Português (0–10)')
	ipv: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador de Ponto de Virada – Média das Notas de Ponto de Virada do Aluno',
	)
	ian: float = Field(
		...,
		ge=0,
		le=10,
		description='Indicador de Adequação ao Nível – Média das Notas de Adequação do Aluno ao nível atual',
	)

	genero: Literal['f', 'm'] = Field(..., description="Gender: 'f' or 'm'")

	instituicao_tipo: int = Field(..., ge=1, le=7, description='Institution type (1 to 7)')
