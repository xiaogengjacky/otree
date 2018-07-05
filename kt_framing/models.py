from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'kt_framing'
    players_per_group = None
    num_rounds = 1
    indicator = True

class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    q1 = models.StringField(
        choices=['33%的概率获得2500元，66%的概率获得2400元，1%的概率获得0元', '确定获得2400元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q2 = models.StringField(
        choices=['33%的概率获得2500元，67%的概率获得0元', '34%的概率获得2400元，66%的概率获得0元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q3 = models.StringField(
        choices=['80%的概率获得4000元，20%的概率获得0元', '确定获得3000元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q4 = models.StringField(
        choices=['20%的概率获得4000元，80%的概率获得0元', '25%的概率获得3000元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q6 = models.StringField(
        choices=['5%的概率获得英法意三国十五日游', '10%的概率获得英国五日游'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q5 = models.StringField(
        choices=['50%的概率获得英法意三国十五日游', '确定获得英国五日游'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q7 = models.StringField(
        choices=['45%的概率获得6000元，55%的概率获得0元', '90%的概率获得3000元，10%的概率获得0元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q8 = models.StringField(
        choices=['0.1%的概率获得6000元，99.9%的概率获得0元', '0.2%的概率获得3000元，99.8%的概率获得0元'],
        verbose_name='请在下列两个选项中选择一个',
        widget=widgets.RadioSelect)

    q11 = models.StringField(
        choices=['50%的概率获得1000元，50%的概率获得0元', '确定获得500元'],
        verbose_name='假设除了你现在拥有的钱之外，你又额外收到了1000元，现在你要在以下两个选项中选择一个',
        widget=widgets.RadioSelect)

    q12 = models.StringField(
        choices=['50%的概率丢掉1000元，50%的概率丢掉0元', '确定丢掉500元'],
        verbose_name='假设除了你现在拥有的钱之外，你又额外收到了2000元，现在你要在以下两个选项中选择一个',
        widget=widgets.RadioSelect)

    # crt_bat = models.PositiveIntegerField(
    #     verbose_name='''
    #     A bat and a ball cost 22 dollars in total.
    #     The bat costs 20 dollars more than the ball.
    #     How many dollars does the ball cost?'''
    # )
    #
    # crt_widget = models.PositiveIntegerField(
    #     verbose_name='''
    #     "If it takes 5 machines 5 minutes to make 5 widgets,
    #     how many minutes would it take 100 machines to make 100 widgets?"
    #     '''
    # )
    #
    # crt_lake = models.PositiveIntegerField(
    #     verbose_name='''
    #     In a lake, there is a patch of lily pads.
    #     Every day, the patch doubles in size.
    #     If it takes 48 days for the patch to cover the entire lake,
    #     how many days would it take for the patch to cover half of the lake?
    #     '''
    # )
