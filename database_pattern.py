import tortoise
from tortoise import Tortoise, run_async
from tortoise import fields
from tortoise.models import Model



class Users(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True)
    name = fields.CharField(50)
    balance = fields.BigIntField(default=0)
    donut = fields.IntField(default=0)
    happiness = fields.IntField(default=10)
    hunger = fields.IntField(default=10)
    health = fields.IntField(default=10)
    energy = fields.IntField(default=10)
    train = fields.BooleanField(default=0)
    enimal = fields.CharField(50, default="")
    nickname = fields.CharField(50, default="")


    class Meta:
        table = 'user_info'

    def __str__(self):
        return self.name

class UsersBoolean(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True)
    train_flag = fields.BooleanField(default=0)


    class Meta:
        table = 'user_boolean'

    def __str__(self):
        return self.name


class GameValues(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(null=True)

    milk = fields.IntField(default=0)
    carrot = fields.IntField(default=0)
    bread = fields.IntField(default=0)
    agg = fields.IntField(default=0)
    cake = fields.IntField(default=0)
    rice = fields.IntField(default=0)
    pizza = fields.IntField(default=0)
    milk = fields.IntField(default=0)
    leg = fields.IntField(default=0)
    meat = fields.IntField(default=0)

    injector = fields.IntField(default=0)
    tablet = fields.IntField(default=0)


    class Meta:
        table = 'user_values'

    def __str__(self):
        return self.name

async def init_db():

    await Tortoise.init(
        db_url='mysql://maslinka:897555887Dan!@91.210.170.247:3306/test',
        modules={'models': ['database_pattern']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    # await Tortoise.a


