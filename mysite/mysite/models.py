# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class RobotAna(models.Model):
    stock_id = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=10)
    m0 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    m6 = models.FloatField()
    m7 = models.FloatField()
    m8 = models.FloatField()
    m9 = models.FloatField()
    m10 = models.FloatField()
    m11 = models.FloatField()
    m12 = models.FloatField()
    a1 = models.CharField(max_length=5)
    a2 = models.CharField(max_length=5)
    a3 = models.CharField(max_length=5)
    a4 = models.CharField(max_length=5)
    a5 = models.CharField(max_length=5)
    type = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'robot_ana'


class RobotAnalysis(models.Model):
    stock_name = models.CharField(max_length=10)
    m0 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    m6 = models.FloatField()
    m7 = models.FloatField()
    m8 = models.FloatField()
    m9 = models.FloatField()
    m10 = models.FloatField()
    m11 = models.FloatField()
    m12 = models.FloatField()
    a1 = models.CharField(max_length=5)
    a2 = models.CharField(max_length=5)
    a3 = models.CharField(max_length=5)
    a4 = models.CharField(max_length=5)
    a5 = models.CharField(max_length=5)
    type = models.CharField(max_length=5)
    stock_id = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_analysis'


class RobotAnalysis2(models.Model):
    stock_id = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=10)
    m0 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    m6 = models.FloatField()
    m7 = models.FloatField()
    m8 = models.FloatField()
    m9 = models.FloatField()
    m10 = models.FloatField()
    m11 = models.FloatField()
    m12 = models.FloatField()
    a1 = models.CharField(max_length=5)
    a2 = models.CharField(max_length=5)
    a3 = models.CharField(max_length=5)
    a4 = models.CharField(max_length=5)
    a5 = models.CharField(max_length=5)
    type = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'robot_analysis2'


class RobotApple(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'robot_apple'


class RobotBalancesheet(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    current_assets = models.CharField(max_length=15)
    cash_equivalents = models.CharField(max_length=15)
    inventory = models.CharField(max_length=15)
    non_current_assets = models.CharField(max_length=15)
    long_term_investment = models.CharField(max_length=15)
    fixed_assets = models.CharField(max_length=15)
    total_assets = models.CharField(max_length=15)
    current_liabilities = models.CharField(max_length=15)
    account_payable = models.CharField(max_length=15)
    non_current_liabilities = models.CharField(max_length=15)
    long_term_liabilities = models.CharField(max_length=15)
    total_liabilities = models.CharField(max_length=15)
    capital = models.CharField(max_length=15)
    total_equity = models.CharField(max_length=15)
    bps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_balancesheet'


class RobotBalancesheetQ(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    current_assets = models.CharField(max_length=15)
    cash_equivalents = models.CharField(max_length=15)
    inventory = models.CharField(max_length=15)
    non_current_assets = models.CharField(max_length=15)
    long_term_investment = models.CharField(max_length=15)
    fixed_assets = models.CharField(max_length=15)
    total_assets = models.CharField(max_length=15)
    current_liabilities = models.CharField(max_length=15)
    account_payable = models.CharField(max_length=15)
    non_current_liabilities = models.CharField(max_length=15)
    long_term_liabilities = models.CharField(max_length=15)
    total_liabilities = models.CharField(max_length=15)
    capital = models.CharField(max_length=15)
    total_equity = models.CharField(max_length=15)
    bps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_balancesheet_q'


class RobotCashFlows(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    income_before_tax = models.CharField(max_length=15)
    cf_operating_activities = models.CharField(db_column='CF_operating_activities', max_length=15)  # Field name made lowercase.
    cf_investing_activities = models.CharField(db_column='CF_investing_activities', max_length=15)  # Field name made lowercase.
    cf_financing_activities = models.CharField(db_column='CF_financing_activities', max_length=15)  # Field name made lowercase.
    net_cash_flows_accumulation = models.CharField(max_length=15)
    free_cash_flows = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_cash_flows'


class RobotCashFlowsQ(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    income_before_tax = models.CharField(max_length=15)
    cf_operating_activities = models.CharField(db_column='CF_operating_activities', max_length=15)  # Field name made lowercase.
    cf_investing_activities = models.CharField(db_column='CF_investing_activities', max_length=15)  # Field name made lowercase.
    cf_financing_activities = models.CharField(db_column='CF_financing_activities', max_length=15)  # Field name made lowercase.
    net_cash_flows = models.CharField(max_length=15)
    free_cash_flows = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_cash_flows_q'


class RobotCategory(models.Model):
    category_id = models.CharField(primary_key=True, max_length=2)
    category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_category'


class RobotCategoryA(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_category_a'


class RobotCategoryB(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    cat_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_category_b'


class RobotCna(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    source = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'robot_cna'


class RobotComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    discuss_id = models.CharField(max_length=8)
    content = models.TextField()
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_comment'


class RobotCorporate(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    foreign_net = models.FloatField()
    foreign_paper = models.CharField(max_length=12)
    foreign_ratio = models.CharField(max_length=12)
    trust_net = models.FloatField()
    trust_paper = models.CharField(max_length=12)
    trust_ratio = models.CharField(max_length=12)
    dealer_net = models.CharField(max_length=12)
    dealer_paper = models.CharField(max_length=12)
    dealer_ratio = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'robot_corporate'


class RobotDiscuss(models.Model):
    discuss_id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=8)
    title = models.CharField(max_length=20)
    content = models.TextField()
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    like = models.IntegerField(blank=True, null=True)
    reply_times = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_discuss'


class RobotDividendPolicy(models.Model):
    year = models.CharField(max_length=5)
    stock_id = models.CharField(max_length=8)
    cash_dividend = models.CharField(max_length=15)
    stock_dividend = models.CharField(max_length=15)
    total_dividend = models.CharField(max_length=15)
    cash_dividend_ratio = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_dividend_policy'


class RobotEconomic(models.Model):
    name = models.CharField(max_length=50)
    explain1 = models.TextField()
    explain2 = models.TextField()
    category = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'robot_economic'


class RobotFive(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    the_open = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()
    item_x = models.FloatField(db_column='Item_x')  # Field name made lowercase.
    price_y = models.FloatField(db_column='Price_y')  # Field name made lowercase.
    price_log_y = models.FloatField(db_column='Price_log_y')  # Field name made lowercase.
    a = models.FloatField()
    b = models.FloatField()
    price_tl = models.FloatField(db_column='Price_TL')  # Field name made lowercase.
    y_tl = models.FloatField(db_column='y_TL')  # Field name made lowercase.
    sd = models.FloatField(db_column='SD')  # Field name made lowercase.
    tl_2sd = models.FloatField(db_column='TL_2SD')  # Field name made lowercase.
    tl_sd = models.FloatField(db_column='TL_SD')  # Field name made lowercase.
    tl_plus_sd = models.FloatField(db_column='TL_plus_SD')  # Field name made lowercase.
    tl_plus_2sd = models.FloatField(db_column='TL_plus_2SD')  # Field name made lowercase.
    sad_95 = models.FloatField()
    sad_75 = models.FloatField()
    happy_75 = models.FloatField()
    happy_95 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'robot_five'


class RobotFq(models.Model):
    fq_id = models.CharField(max_length=2)
    fq_question = models.TextField()
    fq_choice1 = models.CharField(max_length=50)
    fq_choice2 = models.CharField(max_length=50)
    fq_choice3 = models.CharField(max_length=50)
    fq_choice4 = models.CharField(max_length=50, blank=True, null=True)
    fq_choice5 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_fq'


class RobotFqType(models.Model):
    type_id = models.CharField(primary_key=True, max_length=2)
    type_name = models.CharField(max_length=20)
    type_describe = models.TextField(blank=True, null=True)
    type_score = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_fq_type'


class RobotFundSet2016(models.Model):
    name = models.CharField(max_length=30)
    percent = models.FloatField()
    invest = models.CharField(max_length=10)
    number = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_fund_set_2016'


class RobotFundSetHistory(models.Model):
    season = models.CharField(max_length=10)
    invest = models.TextField()
    initial = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_fund_set_history'


class RobotIncomeStatement(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    net_operating_revenues = models.CharField(max_length=15)
    net_gross_profit = models.CharField(max_length=15)
    operating_income = models.CharField(max_length=15)
    income_before_tax = models.CharField(max_length=15)
    net_income = models.CharField(max_length=15)
    eps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_income_statement'


class RobotIncomeStatementQ(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    net_operating_revenues = models.CharField(max_length=15)
    net_gross_profit = models.CharField(max_length=15)
    operating_income = models.CharField(max_length=15)
    income_before_tax = models.CharField(max_length=15)
    net_income = models.CharField(max_length=15)
    eps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_income_statement_q'


class RobotInformation(models.Model):
    stock_id = models.CharField(primary_key=True, max_length=8)
    co_name = models.CharField(max_length=12)
    co_market = models.CharField(max_length=5)
    co_tel = models.CharField(max_length=20)
    co_fax = models.CharField(max_length=20)
    co_website = models.CharField(max_length=50)
    co_cheif = models.CharField(max_length=30)
    co_president = models.CharField(max_length=30)
    co_speaker = models.CharField(max_length=30)
    co_capital = models.CharField(max_length=15)
    co_fullname = models.CharField(max_length=30)
    co_add = models.CharField(max_length=60)
    co_year = models.CharField(max_length=6)
    category = models.CharField(max_length=3)
    score = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_information'


class RobotListedShares(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    stock_num = models.CharField(max_length=5)
    stock_name = models.CharField(max_length=10)
    listed = models.CharField(max_length=3)
    industry = models.CharField(max_length=10)
    listed_date = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_listed_shares'


class RobotMargin(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    margin_balance = models.CharField(max_length=12)
    margin_decrease = models.CharField(max_length=12)
    margin_used = models.CharField(max_length=12)
    stockloan_balance = models.CharField(max_length=12)
    stockloan_decrease = models.CharField(max_length=12)
    stockloan_used = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'robot_margin'


class RobotMarketinformation(models.Model):
    market_id = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    index = models.CharField(max_length=10)
    buy_trans_num = models.CharField(max_length=10)
    buy_trading_volume = models.CharField(max_length=10)
    sell_trans_num = models.CharField(max_length=10)
    sell_trading_volume = models.CharField(max_length=10)
    trans_num = models.CharField(max_length=10)
    trading_volume = models.CharField(max_length=10)
    turnover_in_value = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_marketinformation'


class RobotMean(models.Model):
    m0 = models.FloatField()
    m1 = models.FloatField()
    m2 = models.FloatField()
    m3 = models.FloatField()
    m4 = models.FloatField()
    m5 = models.FloatField()
    m6 = models.FloatField()
    m7 = models.FloatField()
    m8 = models.FloatField()
    m9 = models.FloatField()
    m10 = models.FloatField()
    m11 = models.FloatField()
    m12 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'robot_mean'


class RobotMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=12)
    type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_member'


class RobotMonthrevenue(models.Model):
    stock_id = models.CharField(max_length=8)
    yyyymm = models.CharField(max_length=10)
    month_revenue = models.CharField(max_length=10)
    month_growth = models.CharField(max_length=8)
    year_growth = models.CharField(max_length=8)
    cum_revenue = models.CharField(max_length=16)
    cum_year_growth = models.CharField(max_length=8)
    earning = models.CharField(max_length=10)
    eps = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_monthrevenue'


class RobotNews2330(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_news_2330'


class RobotNews2498(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_news_2498'


class RobotNews3008(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_news_3008'


class RobotNewsIndex(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_news_index'


class RobotOverTheCounterShares(models.Model):
    stock_id = models.IntegerField(primary_key=True)
    stock_num = models.CharField(max_length=5)
    stock_name = models.CharField(max_length=10)
    listed = models.CharField(max_length=3)
    industry = models.CharField(max_length=10)
    listed_date = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'robot_over_the_counter_shares'


class RobotPe(models.Model):
    stock_id = models.CharField(max_length=8)
    date = models.CharField(max_length=10)
    the_close = models.CharField(max_length=10)
    coporate_estimated = models.CharField(max_length=10)
    pe_for_four_season = models.CharField(max_length=10)
    pe_high = models.CharField(max_length=10)
    pe_low = models.CharField(max_length=10)
    eps = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_pe'


class RobotRatio1(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    gross_margin = models.CharField(max_length=8)
    operating_profit_ratio = models.CharField(max_length=8)
    pretax_net_profit_margin = models.CharField(max_length=8)
    net_profit_margin = models.CharField(max_length=8)
    roe = models.CharField(db_column='ROE', max_length=8)  # Field name made lowercase.
    roa = models.CharField(db_column='ROA', max_length=8)  # Field name made lowercase.
    ps_sales = models.CharField(max_length=8)
    bps = models.CharField(max_length=8)
    eps = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio1'


class RobotRatio1Q(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    gross_margin = models.CharField(max_length=8)
    operating_profit_ratio = models.CharField(max_length=8)
    pretax_net_profit_margin = models.CharField(max_length=8)
    net_profit_margin = models.CharField(max_length=8)
    roe = models.CharField(db_column='ROE', max_length=8)  # Field name made lowercase.
    roa = models.CharField(db_column='ROA', max_length=8)  # Field name made lowercase.
    ps_sales = models.CharField(max_length=8)
    bps = models.CharField(max_length=8)
    eps = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio1_q'


class RobotRatio2(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    revenue_growth_ratio = models.CharField(max_length=8)
    operating_profit_growth_ratio = models.CharField(max_length=8)
    pretax_net_profit_growth_margin = models.CharField(max_length=8)
    net_profit_growth_margin = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio2'


class RobotRatio2Q(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    revenue_growth_ratio = models.CharField(max_length=8)
    operating_profit_growth_ratio = models.CharField(max_length=8)
    pretax_net_profit_growth_margin = models.CharField(max_length=8)
    net_profit_growth_margin = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio2_q'


class RobotRatio3(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    accounts_receivable_turnover_ratio = models.CharField(max_length=8)
    accounts_payable_turnover_ratio = models.CharField(max_length=8)
    inventory_turnover_ratio = models.CharField(max_length=8)
    fixed_asset_turnover_ratio = models.CharField(max_length=8)
    total_asset_turnover_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio3'


class RobotRatio3Q(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    accounts_receivable_turnover_ratio = models.CharField(max_length=8)
    accounts_payable_turnover_ratio = models.CharField(max_length=8)
    inventory_turnover_ratio = models.CharField(max_length=8)
    fixed_asset_turnover_ratio = models.CharField(max_length=8)
    total_asset_turnover_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio3_q'


class RobotRatio4(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    current_ratio = models.CharField(max_length=8)
    quick_ratio = models.CharField(max_length=8)
    interest_cover = models.CharField(max_length=20)
    debt_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio4'


class RobotRatio4Q(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    current_ratio = models.CharField(max_length=8)
    quick_ratio = models.CharField(max_length=8)
    interest_cover = models.CharField(max_length=20)
    debt_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'robot_ratio4_q'


class RobotReturn(models.Model):
    re = models.FloatField()

    class Meta:
        managed = False
        db_table = 'robot_return'


class RobotSaveFund(models.Model):
    name = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    invest = models.CharField(max_length=30)
    strategy = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_save_fund'


class RobotStockList(models.Model):
    list_id = models.CharField(max_length=15)
    list_name = models.CharField(max_length=15)
    member_id = models.CharField(max_length=15)
    context_id = models.CharField(max_length=4)
    context_ope = models.CharField(max_length=6)
    context_num = models.CharField(max_length=10)
    context = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'robot_stock_list'


class RobotStocks(models.Model):
    stock_num = models.CharField(max_length=8)
    type = models.CharField(max_length=3, blank=True, null=True)
    num_id = models.CharField(primary_key=True, max_length=8)
    credit_type = models.CharField(max_length=3)
    category = models.CharField(max_length=8)
    big = models.CharField(max_length=2)
    elec = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'robot_stocks'


class RobotTechnologyIndex(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    day_k = models.CharField(db_column='day_K', max_length=8)  # Field name made lowercase.
    day_d = models.CharField(db_column='day_D', max_length=8)  # Field name made lowercase.
    day_macd = models.CharField(db_column='day_MACD', max_length=8)  # Field name made lowercase.
    day_rsi5 = models.CharField(db_column='day_RSI5', max_length=8)  # Field name made lowercase.
    day_rsi10 = models.CharField(db_column='day_RSI10', max_length=8)  # Field name made lowercase.
    week_k = models.CharField(db_column='week_K', max_length=8)  # Field name made lowercase.
    week_d = models.CharField(db_column='week_D', max_length=8)  # Field name made lowercase.
    week_macd = models.CharField(db_column='week_MACD', max_length=8)  # Field name made lowercase.
    week_rsi5 = models.CharField(db_column='week_RSI5', max_length=8)  # Field name made lowercase.
    week_rsi10 = models.CharField(db_column='week_RSI10', max_length=8)  # Field name made lowercase.
    month_k = models.CharField(db_column='month_K', max_length=8)  # Field name made lowercase.
    month_d = models.CharField(db_column='month_D', max_length=8)  # Field name made lowercase.
    month_macd = models.CharField(db_column='month_MACD', max_length=8)  # Field name made lowercase.
    month_rsi5 = models.CharField(db_column='month_RSI5', max_length=8)  # Field name made lowercase.
    month_rsi10 = models.CharField(db_column='month_RSI10', max_length=8)  # Field name made lowercase.
    q_k = models.CharField(db_column='q_K', max_length=8)  # Field name made lowercase.
    q_d = models.CharField(db_column='q_D', max_length=8)  # Field name made lowercase.
    q_rsi5 = models.CharField(db_column='q_RSI5', max_length=8)  # Field name made lowercase.
    q_rsi10 = models.CharField(db_column='q_RSI10', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'robot_technology_index'


class RobotTechnologyIndex2(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    day_k = models.CharField(db_column='day_K', max_length=8)  # Field name made lowercase.
    day_d = models.CharField(db_column='day_D', max_length=8)  # Field name made lowercase.
    day_macd = models.CharField(db_column='day_MACD', max_length=8)  # Field name made lowercase.
    day_rsi5 = models.CharField(db_column='day_RSI5', max_length=8)  # Field name made lowercase.
    day_rsi10 = models.CharField(db_column='day_RSI10', max_length=8)  # Field name made lowercase.
    week_k = models.CharField(db_column='week_K', max_length=8)  # Field name made lowercase.
    week_d = models.CharField(db_column='week_D', max_length=8)  # Field name made lowercase.
    week_macd = models.CharField(db_column='week_MACD', max_length=8)  # Field name made lowercase.
    week_rsi5 = models.CharField(db_column='week_RSI5', max_length=8)  # Field name made lowercase.
    week_rsi10 = models.CharField(db_column='week_RSI10', max_length=8)  # Field name made lowercase.
    month_k = models.CharField(db_column='month_K', max_length=8)  # Field name made lowercase.
    month_d = models.CharField(db_column='month_D', max_length=8)  # Field name made lowercase.
    month_macd = models.CharField(db_column='month_MACD', max_length=8)  # Field name made lowercase.
    month_rsi5 = models.CharField(db_column='month_RSI5', max_length=8)  # Field name made lowercase.
    month_rsi10 = models.CharField(db_column='month_RSI10', max_length=8)  # Field name made lowercase.
    q_k = models.CharField(db_column='q_K', max_length=8)  # Field name made lowercase.
    q_d = models.CharField(db_column='q_D', max_length=8)  # Field name made lowercase.
    q_rsi5 = models.CharField(db_column='q_RSI5', max_length=8)  # Field name made lowercase.
    q_rsi10 = models.CharField(db_column='q_RSI10', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'robot_technology_index2'


class RobotTest1(models.Model):
    test_year = models.CharField(max_length=10)
    test_m1 = models.IntegerField(blank=True, null=True)
    test_m2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_test1'


class RobotTest2(models.Model):
    test_year = models.CharField(max_length=10)
    test_m = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_test2'


class RobotTrackStock(models.Model):
    member_id = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=10, blank=True, null=True)
    list_id = models.CharField(max_length=5, blank=True, null=True)
    list_name = models.CharField(max_length=10, blank=True, null=True)
    stock_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_track_stock'


class RobotTrade2015(models.Model):
    date = models.CharField(max_length=20)
    sell_stock = models.CharField(max_length=20)
    sell_price = models.CharField(max_length=20)
    stocks = models.CharField(max_length=10)
    net = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'robot_trade_2015'


class RobotTransactionInfo(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    the_open = models.CharField(max_length=8)
    high_price = models.CharField(max_length=8)
    low_price = models.CharField(max_length=8)
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()

    class Meta:
        managed = False
        db_table = 'robot_transaction_info'


class RobotTransactionInfo2(models.Model):
    date = models.CharField(max_length=10)
    stock_id = models.CharField(max_length=8)
    the_open = models.CharField(max_length=8)
    high_price = models.CharField(max_length=8)
    low_price = models.CharField(max_length=8)
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()
    stock_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_transaction_info_2'


class RobotYahoo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'robot_yahoo'


class RobotYahooGlobal(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_global'


class RobotYahooHot(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_hot'


class RobotYahooInfo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_info'


class RobotYahooNew(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_new'


class RobotYahooStock(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_stock'


class RobotYahooTec(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_tec'


class RobotYahooTendency(models.Model):
    category = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=10)
    source = models.CharField(max_length=20)
    tag0 = models.CharField(max_length=10, blank=True, null=True)
    tag1 = models.CharField(max_length=10, blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    img_source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_tendency'


class RobotYahooTra(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'robot_yahoo_tra'
        
        
#討論區
class Discuss(models.Model):
    discuss_id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=8)
    title = models.CharField(max_length=20)
    content = models.TextField(default='')
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    like = models.IntegerField(null=True)
    reply_times = models.IntegerField(null=True)
    time = models.CharField(max_length=20, default='')
    class Meta:
        managed = False
        db_table = 'robot_discuss'
# 討論區回覆  id 文章id 內容 作者id 時間 按讚數

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    discuss_id = models.CharField(max_length=8)
    content = models.TextField(default='')
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20, default='')
    class Meta:
        managed = False
        db_table = 'robot_comment'
