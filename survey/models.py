from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.PositiveIntegerField(
        verbose_name='What is your age?',
        min=13, max=125)

    gender = models.StringField(
        choices=['Male', 'Female'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect)

    major = models.StringField(
        choices=['Economics or Business', 'Science', 'Engineering', 'Social Science'],
        verbose_name='What is your major?',
        widget=widgets.RadioSelect
    )

    race = models.StringField(
        choices=['Chinese', 'Malay', 'Indian', 'Caucasian', 'Other'],
        verbose_name='What is your race?',
        widget=widgets.RadioSelect
    )

    year = models.StringField(
        choices=['Freshman', 'Sophomore', 'Junior', 'Senior', 'Gradate'],
        verbose_name='Which year are you in?',
        widget=widgets.RadioSelect
    )

    familysize = models.PositiveIntegerField(
        verbose_name='Size of Immediate Family Household Including Yourself (not college room-mates):',
        min=1, max=20
    )

    familyincome = models.PositiveIntegerField(
        verbose_name='Approximate Monthly Family Income Level in dollars:',
        min=500, max=50000
    )

    personalspending = models.PositiveIntegerField(
        verbose_name='Monthly Personal Expenditures in SG dollars:',
        min=100, max=20000
    )

    volunteer = models.StringField(
        choices=['yes', 'no'],
        verbose_name='Do you belong to any volunteer group?',
        widget=widgets.RadioSelect
    )

    sa_1 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        verbose_name='In general, I think that a group\'s interest is more important than its individual members\'.',
        widget=widgets.RadioSelect
    )

    sa_2 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        verbose_name='I think I am more risk averse than an average person.',
        widget=widgets.RadioSelect
    )

    sa_3 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        verbose_name='I think being risk averse is better than being risk loving.',
        widget=widgets.RadioSelect
    )

    sa_4 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree'],
        verbose_name='I don\'t like taking responsibilities.',
        widget=widgets.RadioSelect
    )

    sa_5 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree',
                 'does not apply'],
        verbose_name='I tend to be more risk averse when making decisions for my group.',
        widget=widgets.RadioSelect
    )

    sa_6 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree',
                 'does not apply'],
        verbose_name='I would take more risk if I were deciding for myself rather than for my group.',
        widget=widgets.RadioSelect
    )

    sa_7 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree',
                 'does not apply'],
        verbose_name='I believed that my group members chose more risky options than me in experiment 1.',
        widget=widgets.RadioSelect
    )

    sa_8 = models.StringField(
        choices=['strongly disagree', 'somewhat disagree', 'neutral', 'somewhat agree', 'strongly agree',
                 'does not apply'],
        verbose_name='I believed that more than half of the participants in this experiment chose more risky options than me in experiment 1.',
        widget=widgets.RadioSelect
    )

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
