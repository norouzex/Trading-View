from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from extentions.checkCoin import Coinlist
from extentions.addToWallet import WalletManagment
from extentions.validateWallet import ValidateWalletCoin
from extentions.addToWallet import WalletManagment
from extentions.CoinPrice import PriceChecker
# from extentions.watchList import WatchList_checker
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email']


class CreatePaperTradingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def validate(self, data):
        key = list(data)
        print(data)
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
    def validate(self,data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if  Coinlist.check(coin1) and Coinlist.check(coin2):
            return data
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
        else:
            raise serializers.ValidationError("coin1 and coin2 not found")

    class Meta:
        model = Position
        fields = "__all__"

class PositionCloseSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='c')
    def validate(self,data):
        data.update({'status':'c'})
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        print(position.coin2)
        WalletManagment.check(position.coin2, position.amount, position.paper_trading)
        return data
    class Meta:
        model = Position
        fields = ['status',]


class PositionAddSerializer(serializers.ModelSerializer):
    paper_trading = serializers.ReadOnlyField(source='paper_trading.id')
    status = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    def validate(self,data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        if  Coinlist.check(coin1) and Coinlist.check(coin2):
            user_id = self.context['request'].user.id
            paper_trading = Paper_trading.objects.get(user__id=user_id)
            if data['order_type'] =="l":
                data.update({'status':'w'})
                if data['trade_type'] == "b":
                    is_valid = ValidateWalletCoin.check(data['coin2'], data['amount'], user_id)
                    if is_valid== True :
                        WalletManagment.check(coin2, data['amount']*-1, paper_trading)
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)
                elif data['trade_type'] == "s":
                    is_valid = ValidateWalletCoin.check(data['coin1'], data['amount'], user_id)
                    if is_valid == True :
                        WalletManagment.check(coin1, data['amount']*-1, paper_trading)
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)
            elif data['order_type'] == "m":
                price = PriceChecker.check_price(coin1, coin2)
                if data['trade_type'] == "b":
                    is_valid = ValidateWalletCoin.check(data['coin2'], data['amount'], user_id)
                    if is_valid== True :
                        coin_amount = data['amount'] / PriceChecker.check_price(coin1, coin2)
                        WalletManagment.check(coin2, data['amount']*-1, paper_trading)
                        WalletManagment.check(coin1, coin_amount, paper_trading)
                        data.update({'status':'d'})
                        data.update({'entert_price':price})
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)
                elif data['trade_type'] == "s":
                    coin_amount = data['amount'] * price
                    is_valid = ValidateWalletCoin.check(data['coin1'], data['amount'], user_id)
                    if is_valid == True :
                        WalletManagment.check(coin1, data['amount']*-1, paper_trading)
                        WalletManagment.check(coin2, coin_amount, paper_trading)
                        data.update({'status':'d'})
                        data.update({'entert_price':price})
                        return data
                    else:
                        raise serializers.ValidationError(is_valid)


                
            return data
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
        else:
            raise serializers.ValidationError("coin1 and coin2 not found")
    class Meta:
        model = Position
        fields = "__all__"


class PositionOptionUpdateSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')
    def validate(self,data):
        user = self.context['request'].user
        new_amount = data['amount']
        # print(new_amount)
        view = self.context.get('view')
        id = view.kwargs['in_position']
        position = Position.objects.get(id=id)
        position_option = Position_option.objects.get(in_position=position)
        wallet = Wallet.objects.get(paper_trading__user=user,coin=position.coin1)
        print(position_option.amount - new_amount)
        print(position.coin1)

        position_amount = position.amount / position.entert_price
        if position_amount>=data['amount'] :
            wallet_result=WalletManagment.check(position.coin1, position_option.amount - new_amount, wallet.paper_trading)
            print(wallet_result)
            if wallet_result == True:
                return data
            else:
                raise serializers.ValidationError(wallet_result)
        else:
            raise serializers.ValidationError("not enough coin")
            

        print(is_valid)
        

    class Meta:
        model = Position_option
        fields ="__all__"

class PositionOptionCreateSerializer(serializers.ModelSerializer):
    in_position = serializers.ReadOnlyField(source='in_position.id')
    trade_type = serializers.ReadOnlyField(source='w')
    oreder_reach_date = serializers.ReadOnlyField(source='')
    status = serializers.ReadOnlyField(source='')
    def validate(self,data):
        user = self.context['request'].user
        view = self.context.get('view')
        id = view.kwargs['pk']
        position = Position.objects.get(id=id)
        wallet = Wallet.objects.get(paper_trading__user=user,coin=position.coin1)
        position_amount = position.amount / position.entert_price
        if position_amount>=data['amount'] :
            wallet_result=WalletManagment.check(position.coin1, data['amount'] * -1, wallet.paper_trading)
            if wallet_result == True:
                if position.order_type == "m":
                    data.update({'status':'w'})
                elif position.order_type == "l":
                    data.update({'status':'p'})
                return data
            else:
                raise serializers.ValidationError(wallet_result)
        else:
            raise serializers.ValidationError("not enough coin in this position")
        

    class Meta:
        model = Position_option
        fields ="__all__"

class WalletSerializer(serializers.ModelSerializer):
    class Meta :
        model =Wallet
        fields = "__all__"

class PositionOptionCloseSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='c')
    trade_type = serializers.ReadOnlyField(source='c')
    def validate(self,data):
        data.update({'status':'c','trade_type':'c'})
        user = self.context['request'].user
        view = self.context.get('view')
        id = view.kwargs['in_position']
        position = Position.objects.get(id=id)
        position_option = Position_option.objects.get(in_position=position)
        # back coin to user wallet after position close
        WalletManagment.check(position.coin1, position_option.amount, position.paper_trading)
        return data
    class Meta:
        model = Position_option
        fields = ['status','trade_type',]

class WatchListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    def validate(self, data):
        coin1 = data['coin1']
        coin2 = data['coin2']
        user = self.context['request'].user



        if not Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 and coin2 not found")
        elif not Coinlist.check(coin1) and Coinlist.check(coin2):
            raise serializers.ValidationError("coin1 not found")
        elif Coinlist.check(coin1) and not Coinlist.check(coin2):
            raise serializers.ValidationError("coin2 not found")
        elif coin1==coin2:
            raise serializers.ValidationError("coin1 and coin2 cant be same")
            

        results=WatchList_checker.check(coin1,coin2,user)
        if not results:
            raise serializers.ValidationError("repeative coin")
        return data
    class Meta:
        model = Watch_list
        fields = "__all__"
