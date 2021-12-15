from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class CreatePaperTradingSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.id')

	def validate(self, data):
		key = list(data)
		
		if not 'balance' in key and 'enter_balance' in key: 
			
			if data['enter_balance']>0.0:
				
				data.update({'balance':data['enter_balance']})
			else:
				raise serializers.ValidationError("enter balance cant be under zero")
			return data

	
	class Meta:
		model = Paper_trading
		fields = ["id","user", 'enter_balance']

class UpdatePaperTradingSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.id')

	def validate(self, data):
		key = list(data)
		
		if 'balance' in key and not 'enter_balance' in key: 
			if data['balance']>=0.0:
				return data
			else:
				raise serializers.ValidationError("enter balance cant be under zero")
		else:
			raise serializers.ValidationError("some thing went wrong")
	class Meta:
		model = Paper_trading
		fields = ["id","user", 'balance']

class PositionSerializer(serializers.ModelSerializer):
	def get_coin1(self, obj):
		return obj.coin1.coin

	def get_coin2(self, obj):
		return obj.coin2.coin
	coin1 = serializers.SerializerMethodField('get_coin1')
	coin2 = serializers.SerializerMethodField('get_coin2')

	class Meta:
		model = Position
		fields = "__all__"


class PositionUpdateSerializer(serializers.ModelSerializer):
	status = serializers.ReadOnlyField(source='c')
	class Meta:
		model = Position
		fields = ['status',]


class PositionAddSerializer(serializers.ModelSerializer):
	paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
	class Meta:
		model = Position
		fields = "__all__"


class PositionOptionSerializer(serializers.ModelSerializer):
	in_position = serializers.ReadOnlyField(source='in_position.id')
	trade_type = serializers.ReadOnlyField(source='w')
	oreder_reach_date = serializers.ReadOnlyField(source='')
	status = serializers.ReadOnlyField(source='')
	class Meta:
		model = Position_option
		fields ="__all__"

class WalletSerializer(serializers.ModelSerializer):
	paper_trading = serializers.ReadOnlyField(source='paper_trading.id')

	def validate(self, data):
			
			if data['amount']>0 and not data['coin']==None: 
				return data
			elif data['amount']<=0:
					raise serializers.ValidationError("amount cant be zero or under zero")
			else:
				raise serializers.ValidationError("some thing went wrong")

	class Meta:
		model = Wallet
		fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
	user = serializers.ReadOnlyField(source='user.id')

	class Meta:
		model = Watch_list
		fields = "__all__"
