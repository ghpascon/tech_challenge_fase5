from sqlalchemy import Column, Float, Integer, String

from .mixin import Base, BaseMixin


class Predict(Base, BaseMixin):
	__tablename__ = 'predicts'

	# Primary key
	id = Column(Integer, primary_key=True, autoincrement=True)
	# Input data for prediction
	fase = Column(Float, nullable=False)
	idade = Column(Float, nullable=False)
	iaa = Column(Float, nullable=False)
	ieg = Column(Float, nullable=False)
	ips = Column(Float, nullable=False)
	ipp = Column(Float, nullable=False)
	ida = Column(Float, nullable=False)
	mat = Column(Float, nullable=False)
	por = Column(Float, nullable=False)
	ipv = Column(Float, nullable=False)
	genero = Column(String(1), nullable=False)  # 'f' or 'm'
	instituicao_tipo = Column(Integer, nullable=False)  # 1 to 7
	# Output prediction result
	predict = Column(Float, nullable=False)
