# coding=utf-8

from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

'''
-------- stockbasic info --------
'''
class StockBasic(Base):
    """股票列表
    is_hs	    str	N	是否沪深港通标的，N否 H沪股通 S深股通
    list_status	str	N	上市状态： L上市 D退市 P暂停上市
    exchange	str	N	交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    """
    __tablename__ = 'stock_basic'

    ts_code = Column(String(10), primary_key=True)  # TS代码
    symbol = Column(String(10))         # 股票代码
    name = Column(String(10))           # 股票名称
    area = Column(String(4))            # 所在地域
    industry = Column(String(4))        # 所属行业
    fullname = Column(String(30))       # 股票全称
    enname = Column(String(100))        # 英文全称
    market = Column(String(3))          # 市场类型 （主板/中小板/创业板）
    exchange = Column(String(4))        # 交易所代码
    curr_type = Column(String(3))       # 交易货币
    list_status = Column(String(1))     # 上市状态： L上市 D退市 P暂停上市
    list_date = Column(String(8))       # 上市日期
    delist_date = Column(String(8))     # 退市日期
    is_hs = Column(String(1))           # 是否沪深港通标的，N否 H沪股通 S深股通

'''
-------- daily info --------
'''
class Daily(Base):
    """日线行情
    ts_code	str	N	股票代码（二选一）
    trade_date	str	N	交易日期（二选一）
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'daily'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    trade_date = Column(String(8), primary_key=True)    # 交易日期
    open = Column(Float)        # 开盘价
    high = Column(Float)        # 最高价
    low = Column(Float)         # 最低价
    close = Column(Float)       # 收盘价
    pre_close = Column(Float)   # 昨收价
    change = Column(Float)      # 涨跌额
    pct_chg = Column(Float)     # 涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol = Column(Float)         # 成交量 （手）
    amount = Column(Float)      # 成交额 （千元）

'''
-------- financial info --------
'''
class income(Base):
    """
    ts_code	str	str Y	股票代码
    trade_date	str	N	交易日期
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'income'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    f_ann_date = Column(String(8))                      # 实际公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    report_type = Column(String(2), primary_key=True)   # 报告类型
    comp_type = Column(Float)   # 公司类型（1一般工商业，2银行，3保险，4证券）
    basic_eps = Column(Float)  # 基本每股收益
    diluted_eps = Column(Float)  # 稀释每股收益
    total_revenue = Column(Float)  # 营业总收入
    revenue = Column(Float)  # 营业收入
    int_income = Column(Float)  # 利息收入
    prem_earned = Column(Float)  # 已赚保费
    comm_income = Column(Float)  # 手续费及佣金收入
    n_commis_income = Column(Float)  # 手续费及佣金净收入
    n_oth_income = Column(Float)  # 其他经营净收益
    n_oth_b_income = Column(Float)  # 加:其他业务净收益
    prem_income = Column(Float)  # 保险业务收入
    out_prem = Column(Float)  # 减:分出保费
    une_prem_reser = Column(Float)  # 提取未到期责任准备金
    reins_income = Column(Float)  # 其中:分保费收入
    n_sec_tb_income = Column(Float)  # 代理买卖证券业务净
    n_sec_uw_income = Column(Float)  # 证券承销业务净收入
    n_asset_mg_income = Column(Float)  # 受托客户资产管理业务净收入
    oth_b_income = Column(Float)  # 其他业务收入
    fv_value_chg_gain = Column(Float)  # 加:公允价值变动净收益
    invest_income = Column(Float)  # 加:投资净收益
    ass_invest_income = Column(Float)  # 其中:对联营企业和合营企业的投资收益
    forex_gain = Column(Float)  # 加:汇兑净收益
    total_cogs = Column(Float)  # 营业总成本
    oper_cost = Column(Float)  # 减:营业成本
    int_exp = Column(Float)  # 减:利息支出
    comm_exp = Column(Float)  # 减:手续费及佣金支出
    biz_tax_surchg = Column(Float)  # 减:营业税金及附加
    sell_exp = Column(Float)  # 减:销售费用
    admin_exp = Column(Float)  # 减:管理费用
    fin_exp = Column(Float)  # 减:财务费用
    assets_impair_loss = Column(Float)  # 减:资产减值损失
    prem_refund = Column(Float)  # 退保金
    compens_payout = Column(Float)  # 赔付总支出
    reser_insur_liab = Column(Float)  # 提取保险责任准备金
    div_payt = Column(Float)  # 保户红利支出
    reins_exp = Column(Float)  # 分保费用
    oper_exp = Column(Float)  # 营业支出
    compens_payout_refu = Column(Float)  # 减:摊回赔付支出
    insur_reser_refu = Column(Float)  # 减:摊回保险责任准备金
    reins_cost_refund = Column(Float)  # 减:摊回分保费用
    other_bus_cost = Column(Float)  # 其他业务成本
    operate_profit = Column(Float)  # 营业利润
    non_oper_income = Column(Float)  # 加:营业外收入
    non_oper_exp = Column(Float)  # 减:营业外支出
    nca_disploss = Column(Float)  # 其中:减:非流动资产处置净损失
    total_profit = Column(Float)  # 利润总额
    income_tax = Column(Float)  # 所得税费用
    n_income = Column(Float)  # 净利润(含少数股东损益)
    n_income_attr_p = Column(Float)  # 净利润(不含少数股东损益)
    minority_gain = Column(Float)  # 少数股东损益
    oth_compr_income = Column(Float)  # 其他综合收益
    t_compr_income = Column(Float)  # 综合收益总额
    compr_inc_attr_p = Column(Float)  # 归属于母公司(或股东)的综合收益总额
    compr_inc_attr_m_s = Column(Float)  # 归属于少数股东的综合收益总额
    ebit = Column(Float)  # 息税前利润
    ebitda = Column(Float)  # 息税折旧摊销前利润
    insurance_exp = Column(Float)  # 保险业务支出
    undist_profit = Column(Float)  # 年初未分配利润
    distable_profit = Column(Float)  # 可分配利润
    update_flag = Column(String(1))  # 更新标识，0未修改，1更正过


class balancesheet(Base):
    """
    ts_code	str	str Y	股票代码
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'balancesheet'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    f_ann_date = Column(String(8))                      # 实际公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    report_type = Column(String(2), primary_key=True)   # 报告类型
    comp_type = Column(Float)   # 公司类型（1一般工商业，2银行，3保险，4证券）
    total_share = Column(Float)  # 期末总股本
    cap_rese = Column(Float)  # 资本公积金
    undistr_porfit = Column(Float)  # 未分配利润
    surplus_rese = Column(Float)  # 盈余公积金
    special_rese = Column(Float)  # 专项储备
    money_cap = Column(Float)  # 货币资金
    trad_asset = Column(Float)  # 交易性金融资产
    notes_receiv = Column(Float)  # 应收票据
    accounts_receiv = Column(Float)  # 应收账款
    oth_receiv = Column(Float)  # 其他应收款
    prepayment = Column(Float)  # 预付款项
    div_receiv = Column(Float)  # 应收股利
    int_receiv = Column(Float)  # 应收利息
    inventories = Column(Float)  # 存货
    amor_exp = Column(Float)  # 待摊费用
    nca_within_1y = Column(Float)  # 一年内到期的非流动资产
    sett_rsrv = Column(Float)  # 结算备付金
    loanto_oth_bank_fi = Column(Float)  # 拆出资金
    premium_receiv = Column(Float)  # 应收保费
    reinsur_receiv = Column(Float)  # 应收分保账款
    reinsur_res_receiv = Column(Float)  # 应收分保合同准备金
    pur_resale_fa = Column(Float)  # 买入返售金融资产
    oth_cur_assets = Column(Float)  # 其他流动资产
    total_cur_assets = Column(Float)  # 流动资产合计
    fa_avail_for_sale = Column(Float)  # 可供出售金融资产
    htm_invest = Column(Float)  # 持有至到期投资
    lt_eqt_invest = Column(Float)  # 长期股权投资
    invest_real_estate = Column(Float)  # 投资性房地产
    time_deposits = Column(Float)  # 定期存款
    oth_assets = Column(Float)  # 其他资产
    lt_rec = Column(Float)  # 长期应收款
    fix_assets = Column(Float)  # 固定资产
    cip = Column(Float)  # 在建工程
    const_materials = Column(Float)  # 工程物资
    fixed_assets_disp = Column(Float)  # 固定资产清理
    produc_bio_assets = Column(Float)  # 生产性生物资产
    oil_and_gas_assets = Column(Float)  # 油气资产
    intan_assets = Column(Float)  # 无形资产
    r_and_d = Column(Float)  # 研发支出
    goodwill = Column(Float)  # 商誉
    lt_amor_exp = Column(Float)  # 长期待摊费用
    defer_tax_assets = Column(Float)  # 递延所得税资产
    decr_in_disbur = Column(Float)  # 发放贷款及垫款
    oth_nca = Column(Float)  # 其他非流动资产
    total_nca = Column(Float)  # 非流动资产合计
    cash_reser_cb = Column(Float)  # 现金及存放中央银行款项
    depos_in_oth_bfi = Column(Float)  # 存放同业和其它金融机构款项
    prec_metals = Column(Float)  # 贵金属
    deriv_assets = Column(Float)  # 衍生金融资产
    rr_reins_une_prem = Column(Float)  # 应收分保未到期责任准备金
    rr_reins_outstd_cla = Column(Float)  # 应收分保未决赔款准备金
    rr_reins_lins_liab = Column(Float)  # 应收分保寿险责任准备金
    rr_reins_lthins_liab = Column(Float)  # 应收分保长期健康险责任准备金
    refund_depos = Column(Float)  # 存出保证金
    ph_pledge_loans = Column(Float)  # 保户质押贷款
    refund_cap_depos = Column(Float)  # 存出资本保证金
    indep_acct_assets = Column(Float)  # 独立账户资产
    client_depos = Column(Float)  # 其中：客户资金存款
    client_prov = Column(Float)  # 其中：客户备付金
    transac_seat_fee = Column(Float)  # 其中:交易席位费
    invest_as_receiv = Column(Float)  # 应收款项类投资
    total_assets = Column(Float)  # 资产总计
    lt_borr = Column(Float)  # 长期借款
    st_borr = Column(Float)  # 短期借款
    cb_borr = Column(Float)  # 向中央银行借款
    depos_ib_deposits = Column(Float)  # 吸收存款及同业存放
    loan_oth_bank = Column(Float)  # 拆入资金
    trading_fl = Column(Float)  # 交易性金融负债
    notes_payable = Column(Float)  # 应付票据
    acct_payable = Column(Float)  # 应付账款
    adv_receipts = Column(Float)  # 预收款项
    sold_for_repur_fa = Column(Float)  # 卖出回购金融资产款
    comm_payable = Column(Float)  # 应付手续费及佣金
    payroll_payable = Column(Float)  # 应付职工薪酬
    taxes_payable = Column(Float)  # 应交税费
    int_payable = Column(Float)  # 应付利息
    div_payable = Column(Float)  # 应付股利
    oth_payable = Column(Float)  # 其他应付款
    acc_exp = Column(Float)  # 预提费用
    deferred_inc = Column(Float)  # 递延收益
    st_bonds_payable = Column(Float)  # 应付短期债券
    payable_to_reinsurer = Column(Float)  # 应付分保账款
    rsrv_insur_cont = Column(Float)  # 保险合同准备金
    acting_trading_sec = Column(Float)  # 代理买卖证券款
    acting_uw_sec = Column(Float)  # 代理承销证券款
    non_cur_liab_due_1y = Column(Float)  # 一年内到期的非流动负债
    oth_cur_liab = Column(Float)  # 其他流动负债
    total_cur_liab = Column(Float)  # 流动负债合计
    bond_payable = Column(Float)  # 应付债券
    lt_payable = Column(Float)  # 长期应付款
    specific_payables = Column(Float)  # 专项应付款
    estimated_liab = Column(Float)  # 预计负债
    defer_tax_liab = Column(Float)  # 递延所得税负债
    defer_inc_non_cur_liab = Column(Float)  # 递延收益-非流动负债
    oth_ncl = Column(Float)  # 其他非流动负债
    total_ncl = Column(Float)  # 非流动负债合计
    depos_oth_bfi = Column(Float)  # 同业和其它金融机构存放款项
    deriv_liab = Column(Float)  # 衍生金融负债
    depos = Column(Float)  # 吸收存款
    agency_bus_liab = Column(Float)  # 代理业务负债
    oth_liab = Column(Float)  # 其他负债
    prem_receiv_adva = Column(Float)  # 预收保费
    depos_received = Column(Float)  # 存入保证金
    ph_invest = Column(Float)  # 保户储金及投资款
    reser_une_prem = Column(Float)  # 未到期责任准备金
    reser_outstd_claims = Column(Float)  # 未决赔款准备金
    reser_lins_liab = Column(Float)  # 寿险责任准备金
    reser_lthins_liab = Column(Float)  # 长期健康险责任准备金
    indept_acc_liab = Column(Float)  # 独立账户负债
    pledge_borr = Column(Float)  # 其中:质押借款
    indem_payable = Column(Float)  # 应付赔付款
    policy_div_payable = Column(Float)  # 应付保单红利
    total_liab = Column(Float)  # 负债合计
    treasury_share = Column(Float)  # 减:库存股
    ordin_risk_reser = Column(Float)  # 一般风险准备
    forex_differ = Column(Float)  # 外币报表折算差额
    invest_loss_unconf = Column(Float)  # 未确认的投资损失
    minority_int = Column(Float)  # 少数股东权益
    total_hldr_eqy_exc_min_int = Column(Float)  # 股东权益合计(不含少数股东权益)
    total_hldr_eqy_inc_min_int = Column(Float)  # 股东权益合计(含少数股东权益)
    total_liab_hldr_eqy = Column(Float)  # 负债及股东权益总计
    lt_payroll_payable = Column(Float)  # 长期应付职工薪酬
    oth_comp_income = Column(Float)  # 其他综合收益
    oth_eqt_tools = Column(Float)  # 其他权益工具
    oth_eqt_tools_p_shr = Column(Float)  # 其他权益工具(优先股)
    lending_funds = Column(Float)  # 融出资金
    acc_receivable = Column(Float)  # 应收款项
    st_fin_payable = Column(Float)  # 应付短期融资款
    payables = Column(Float)  # 应付款项
    hfs_assets = Column(Float)  # 持有待售的资产
    hfs_sales = Column(Float)  # 持有待售的负债
    update_flag = Column(String(1))  # 更新标识，0未修改，1更正过


class cashflow(Base):
    """
    ts_code	str	str Y	股票代码
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'cashflow'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    f_ann_date = Column(String(8))                      # 实际公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    comp_type = Column(Float)   # 公司类型（1一般工商业，2银行，3保险，4证券）
    report_type = Column(String(2), primary_key=True)  # 报告类型
    net_profit = Column(Float)  # 净利润
    finan_exp = Column(Float)  # 财务费用
    c_fr_sale_sg = Column(Float)  # 销售商品、提供劳务收到的现金
    recp_tax_rends = Column(Float)  # 收到的税费返还
    n_depos_incr_fi = Column(Float)  # 客户存款和同业存放款项净增加额
    n_incr_loans_cb = Column(Float)  # 向中央银行借款净增加额
    n_inc_borr_oth_fi = Column(Float)  # 向其他金融机构拆入资金净增加额
    prem_fr_orig_contr = Column(Float)  # 收到原保险合同保费取得的现金
    n_incr_insured_dep = Column(Float)  # 保户储金净增加额
    n_reinsur_prem = Column(Float)  # 收到再保业务现金净额
    n_incr_disp_tfa = Column(Float)  # 处置交易性金融资产净增加额
    ifc_cash_incr = Column(Float)  # 收取利息和手续费净增加额
    n_incr_disp_faas = Column(Float)  # 处置可供出售金融资产净增加额
    n_incr_loans_oth_bank = Column(Float)  # 拆入资金净增加额
    n_cap_incr_repur = Column(Float)  # 回购业务资金净增加额
    c_fr_oth_operate_a = Column(Float)  # 收到其他与经营活动有关的现金
    c_inf_fr_operate_a = Column(Float)  # 经营活动现金流入小计
    c_paid_goods_s = Column(Float)  # 购买商品、接受劳务支付的现金
    c_paid_to_for_empl = Column(Float)  # 支付给职工以及为职工支付的现金
    c_paid_for_taxes = Column(Float)  # 支付的各项税费
    n_incr_clt_loan_adv = Column(Float)  # 客户贷款及垫款净增加额
    n_incr_dep_cbob = Column(Float)  # 存放央行和同业款项净增加额
    c_pay_claims_orig_inco = Column(Float)  # 支付原保险合同赔付款项的现金
    pay_handling_chrg = Column(Float)  # 支付手续费的现金
    pay_comm_insur_plcy = Column(Float)  # 支付保单红利的现金
    oth_cash_pay_oper_act = Column(Float)  # 支付其他与经营活动有关的现金
    st_cash_out_act = Column(Float)  # 经营活动现金流出小计
    n_cashflow_act = Column(Float)  # 经营活动产生的现金流量净额
    oth_recp_ral_inv_act = Column(Float)  # 收到其他与投资活动有关的现金
    c_disp_withdrwl_invest = Column(Float)  # 收回投资收到的现金
    c_recp_return_invest = Column(Float)  # 取得投资收益收到的现金
    n_recp_disp_fiolta = Column(Float)  # 处置固定资产、无形资产和其他长期资产收回的现金净额
    n_recp_disp_sobu = Column(Float)  # 处置子公司及其他营业单位收到的现金净额
    stot_inflows_inv_act = Column(Float)  # 投资活动现金流入小计
    c_pay_acq_const_fiolta = Column(Float)  # 购建固定资产、无形资产和其他长期资产支付的现金
    c_paid_invest = Column(Float)  # 投资支付的现金
    n_disp_subs_oth_biz = Column(Float)  # 取得子公司及其他营业单位支付的现金净额
    oth_pay_ral_inv_act = Column(Float)  # 支付其他与投资活动有关的现金
    n_incr_pledge_loan = Column(Float)  # 质押贷款净增加额
    stot_out_inv_act = Column(Float)  # 投资活动现金流出小计
    n_cashflow_inv_act = Column(Float)  # 投资活动产生的现金流量净额
    c_recp_borrow = Column(Float)  # 取得借款收到的现金
    proc_issue_bonds = Column(Float)  # 发行债券收到的现金
    oth_cash_recp_ral_fnc_act = Column(Float)  # 收到其他与筹资活动有关的现金
    stot_cash_in_fnc_act = Column(Float)  # 筹资活动现金流入小计
    free_cashflow = Column(Float)  # 企业自由现金流量
    c_prepay_amt_borr = Column(Float)  # 偿还债务支付的现金
    c_pay_dist_dpcp_int_exp = Column(Float)  # 分配股利、利润或偿付利息支付的现金
    incl_dvd_profit_paid_sc_ms = Column(Float)  # 其中:子公司支付给少数股东的股利、利润
    oth_cashpay_ral_fnc_act = Column(Float)  # 支付其他与筹资活动有关的现金
    stot_cashout_fnc_act = Column(Float)  # 筹资活动现金流出小计
    n_cash_flows_fnc_act = Column(Float)  # 筹资活动产生的现金流量净额
    eff_fx_flu_cash = Column(Float)  # 汇率变动对现金的影响
    n_incr_cash_cash_equ = Column(Float)  # 现金及现金等价物净增加额
    c_cash_equ_beg_period = Column(Float)  # 期初现金及现金等价物余额
    c_cash_equ_end_period = Column(Float)  # 期末现金及现金等价物余额
    c_recp_cap_contrib = Column(Float)  # 吸收投资收到的现金
    incl_cash_rec_saims = Column(Float)  # 其中:子公司吸收少数股东投资收到的现金
    uncon_invest_loss = Column(Float)  # 未确认投资损失
    prov_depr_assets = Column(Float)  # 加:资产减值准备
    depr_fa_coga_dpba = Column(Float)  # 固定资产折旧、油气资产折耗、生产性生物资产折旧
    amort_intang_assets = Column(Float)  # 无形资产摊销
    lt_amort_deferred_exp = Column(Float)  # 长期待摊费用摊销
    decr_deferred_exp = Column(Float)  # 待摊费用减少
    incr_acc_exp = Column(Float)  # 预提费用增加
    loss_disp_fiolta = Column(Float)  # 处置固定、无形资产和其他长期资产的损失
    loss_scr_fa = Column(Float)  # 固定资产报废损失
    loss_fv_chg = Column(Float)  # 公允价值变动损失
    invest_loss = Column(Float)  # 投资损失
    decr_def_inc_tax_assets = Column(Float)  # 递延所得税资产减少
    incr_def_inc_tax_liab = Column(Float)  # 递延所得税负债增加
    decr_inventories = Column(Float)  # 存货的减少
    decr_oper_payable = Column(Float)  # 经营性应收项目的减少
    incr_oper_payable = Column(Float)  # 经营性应付项目的增加
    others = Column(Float)  # 其他
    im_net_cashflow_oper_act = Column(Float)  # 经营活动产生的现金流量净额(间接法)
    conv_debt_into_cap = Column(Float)  # 债务转为资本
    conv_copbonds_due_within_1y = Column(Float)  # 一年内到期的可转换公司债券
    fa_fnc_leases = Column(Float)  # 融资租入固定资产
    end_bal_cash = Column(Float)  # 现金的期末余额
    beg_bal_cash = Column(Float)  # 减:现金的期初余额
    end_bal_cash_equ = Column(Float)  # 加:现金等价物的期末余额
    beg_bal_cash_equ = Column(Float)  # 减:现金等价物的期初余额
    im_n_incr_cash_equ = Column(Float)  # 现金及现金等价物净增加额(间接法)
    update_flag = Column(String(1))  # 更新标识，0未修改，1更正过


class forecast(Base):
    """
    ts_code	str	str Y	股票代码
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'forecast'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    type = Column(String(8))  # 业绩预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)
    p_change_min = Column(Float)  # 预告净利润变动幅度下限（%）
    p_change_max = Column(Float)  # 预告净利润变动幅度上限（%）
    net_profit_min = Column(Float)  # 预告净利润下限（万元）
    net_profit_max = Column(Float)  # 预告净利润上限（万元）
    last_parent_net = Column(Float)  # 上年同期归属母公司净利润
    first_ann_date = Column(String(8))  # 首次公告日
    # summary = Column(String(1000))  # 业绩预告摘要
    # change_reason = Column(String(8))  # 业绩变动原因


class express(Base):
    """
    ts_code	str	str Y	股票代码
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'express'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    revenue = Column(Float)  # 营业收入(元)
    operate_profit = Column(Float)  # 营业利润(元)
    total_profit = Column(Float)  # 利润总额(元)
    n_income = Column(Float)  # 净利润(元)
    total_assets = Column(Float)  # 总资产(元)
    total_hldr_eqy_exc_min_int = Column(Float)  # 股东权益合计(不含少数股东权益)(元)
    diluted_eps = Column(Float)  # 每股收益(摊薄)(元)
    diluted_roe = Column(Float)  # 净资产收益率(摊薄)(%)
    yoy_net_profit = Column(Float)  # 去年同期修正后净利润
    bps = Column(Float)  # 每股净资产
    yoy_sales = Column(Float)  # 同比增长率:营业收入
    yoy_op = Column(Float)  # 同比增长率:营业利润
    yoy_tp = Column(Float)  # 同比增长率:利润总额
    yoy_dedu_np = Column(Float)  # 同比增长率:归属母公司股东的净利润
    yoy_eps = Column(Float)  # 同比增长率:基本每股收益
    yoy_roe = Column(Float)  # 同比增减:加权平均净资产收益率
    growth_assets = Column(Float)  # 比年初增长率:总资产
    yoy_equity = Column(Float)  # 比年初增长率:归属母公司的股东权益
    growth_bps = Column(Float)  # 比年初增长率:归属于母公司股东的每股净资产
    or_last_year = Column(Float)  # 去年同期营业收入
    op_last_year = Column(Float)  # 去年同期营业利润
    tp_last_year = Column(Float)  # 去年同期利润总额
    np_last_year = Column(Float)  # 去年同期净利润
    eps_last_year = Column(Float)  # 去年同期每股收益
    open_net_assets = Column(Float)  # 期初净资产
    open_bps = Column(Float)  # 期初每股净资产
    perf_summary = Column(String(8))  # 业绩简要说明
    is_audit = Column(String(1))  # 是否审计： 1是0否
    remark = Column(String(100))  # 备注


class fina_indicator(Base):
    """
    ts_code	str	str Y	股票代码
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'fina_indicator'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    ann_date = Column(String(8))                        # 公告日期
    end_date = Column(String(8), primary_key=True)      # 报告期
    eps = Column(Float)  # 基本每股收益
    dt_eps = Column(Float)  # 稀释每股收益
    total_revenue_ps = Column(Float)  # 每股营业总收入
    revenue_ps = Column(Float)  # 每股营业收入
    capital_rese_ps = Column(Float)  # 每股资本公积
    surplus_rese_ps = Column(Float)  # 每股盈余公积
    undist_profit_ps = Column(Float)  # 每股未分配利润
    extra_item = Column(Float)  # 非经常性损益
    profit_dedt = Column(Float)  # 扣除非经常性损益后的净利润
    gross_margin = Column(Float)  # 毛利
    current_ratio = Column(Float)  # 流动比率
    quick_ratio = Column(Float)  # 速动比率
    cash_ratio = Column(Float)  # 保守速动比率
    invturn_days = Column(Float)  # 存货周转天数
    arturn_days = Column(Float)  # 应收账款周转天数
    inv_turn = Column(Float)  # 存货周转率
    ar_turn = Column(Float)  # 应收账款周转率
    ca_turn = Column(Float)  # 流动资产周转率
    fa_turn = Column(Float)  # 固定资产周转率
    assets_turn = Column(Float)  # 总资产周转率
    op_income = Column(Float)  # 经营活动净收益
    valuechange_income = Column(Float)  # 价值变动净收益
    interst_income = Column(Float)  # 利息费用
    daa = Column(Float)  # 折旧与摊销
    ebit = Column(Float)  # 息税前利润
    ebitda = Column(Float)  # 息税折旧摊销前利润
    fcff = Column(Float)  # 企业自由现金流量
    fcfe = Column(Float)  # 股权自由现金流量
    current_exint = Column(Float)  # 无息流动负债
    noncurrent_exint = Column(Float)  # 无息非流动负债
    interestdebt = Column(Float)  # 带息债务
    netdebt = Column(Float)  # 净债务
    tangible_asset = Column(Float)  # 有形资产
    working_capital = Column(Float)  # 营运资金
    networking_capital = Column(Float)  # 营运流动资本
    invest_capital = Column(Float)  # 全部投入资本
    retained_earnings = Column(Float)  # 留存收益
    diluted2_eps = Column(Float)  # 期末摊薄每股收益
    bps = Column(Float)  # 每股净资产
    ocfps = Column(Float)  # 每股经营活动产生的现金流量净额
    retainedps = Column(Float)  # 每股留存收益
    cfps = Column(Float)  # 每股现金流量净额
    ebit_ps = Column(Float)  # 每股息税前利润
    fcff_ps = Column(Float)  # 每股企业自由现金流量
    fcfe_ps = Column(Float)  # 每股股东自由现金流量
    netprofit_margin = Column(Float)  # 销售净利率
    grossprofit_margin = Column(Float)  # 销售毛利率
    cogs_of_sales = Column(Float)  # 销售成本率
    expense_of_sales = Column(Float)  # 销售期间费用率
    profit_to_gr = Column(Float)  # 净利润/营业总收入
    saleexp_to_gr = Column(Float)  # 销售费用/营业总收入
    adminexp_of_gr = Column(Float)  # 管理费用/营业总收入
    finaexp_of_gr = Column(Float)  # 财务费用/营业总收入
    impai_ttm = Column(Float)  # 资产减值损失/营业总收入
    gc_of_gr = Column(Float)  # 营业总成本/营业总收入
    op_of_gr = Column(Float)  # 营业利润/营业总收入
    ebit_of_gr = Column(Float)  # 息税前利润/营业总收入
    roe = Column(Float)  # 净资产收益率
    roe_waa = Column(Float)  # 加权平均净资产收益率
    roe_dt = Column(Float)  # 净资产收益率(扣除非经常损益)
    roa = Column(Float)  # 总资产报酬率
    npta = Column(Float)  # 总资产净利润
    roic = Column(Float)  # 投入资本回报率
    roe_yearly = Column(Float)  # 年化净资产收益率
    roa2_yearly = Column(Float)  # 年化总资产报酬率
    roe_avg = Column(Float)  # 平均净资产收益率(增发条件)
    opincome_of_ebt = Column(Float)  # 经营活动净收益/利润总额
    investincome_of_ebt = Column(Float)  # 价值变动净收益/利润总额
    n_op_profit_of_ebt = Column(Float)  # 营业外收支净额/利润总额
    tax_to_ebt = Column(Float)  # 所得税/利润总额
    dtprofit_to_profit = Column(Float)  # 扣除非经常损益后的净利润/净利润
    salescash_to_or = Column(Float)  # 销售商品提供劳务收到的现金/营业收入
    ocf_to_or = Column(Float)  # 经营活动产生的现金流量净额/营业收入
    ocf_to_opincome = Column(Float)  # 经营活动产生的现金流量净额/经营活动净收益
    capitalized_to_da = Column(Float)  # 资本支出/折旧和摊销
    debt_to_assets = Column(Float)  # 资产负债率
    assets_to_eqt = Column(Float)  # 权益乘数
    dp_assets_to_eqt = Column(Float)  # 权益乘数(杜邦分析)
    ca_to_assets = Column(Float)  # 流动资产/总资产
    nca_to_assets = Column(Float)  # 非流动资产/总资产
    tbassets_to_totalassets = Column(Float)  # 有形资产/总资产
    int_to_talcap = Column(Float)  # 带息债务/全部投入资本
    eqt_to_talcapital = Column(Float)  # 归属于母公司的股东权益/全部投入资本
    currentdebt_to_debt = Column(Float)  # 流动负债/负债合计
    longdeb_to_debt = Column(Float)  # 非流动负债/负债合计
    ocf_to_shortdebt = Column(Float)  # 经营活动产生的现金流量净额/流动负债
    debt_to_eqt = Column(Float)  # 产权比率
    eqt_to_debt = Column(Float)  # 归属于母公司的股东权益/负债合计
    eqt_to_interestdebt = Column(Float)  # 归属于母公司的股东权益/带息债务
    tangibleasset_to_debt = Column(Float)  # 有形资产/负债合计
    tangasset_to_intdebt = Column(Float)  # 有形资产/带息债务
    tangibleasset_to_netdebt = Column(Float)  # 有形资产/净债务
    ocf_to_debt = Column(Float)  # 经营活动产生的现金流量净额/负债合计
    ocf_to_interestdebt = Column(Float)  # 经营活动产生的现金流量净额/带息债务
    ocf_to_netdebt = Column(Float)  # 经营活动产生的现金流量净额/净债务
    ebit_to_interest = Column(Float)  # 已获利息倍数(EBIT/利息费用)
    longdebt_to_workingcapital = Column(Float)  # 长期债务与营运资金比率
    ebitda_to_debt = Column(Float)  # 息税折旧摊销前利润/负债合计
    turn_days = Column(Float)  # 营业周期
    roa_yearly = Column(Float)  # 年化总资产净利率
    roa_dp = Column(Float)  # 总资产净利率(杜邦分析)
    fixed_assets = Column(Float)  # 固定资产合计
    profit_prefin_exp = Column(Float)  # 扣除财务费用前营业利润
    non_op_profit = Column(Float)  # 非营业利润
    op_to_ebt = Column(Float)  # 营业利润／利润总额
    nop_to_ebt = Column(Float)  # 非营业利润／利润总额
    ocf_to_profit = Column(Float)  # 经营活动产生的现金流量净额／营业利润
    cash_to_liqdebt = Column(Float)  # 货币资金／流动负债
    cash_to_liqdebt_withinterest = Column(Float)  # 货币资金／带息流动负债
    op_to_liqdebt = Column(Float)  # 营业利润／流动负债
    op_to_debt = Column(Float)  # 营业利润／负债合计
    roic_yearly = Column(Float)  # 年化投入资本回报率
    total_fa_trun = Column(Float)  # 固定资产合计周转率
    profit_to_op = Column(Float)  # 利润总额／营业收入
    q_opincome = Column(Float)  # 经营活动单季度净收益
    q_investincome = Column(Float)  # 价值变动单季度净收益
    q_dtprofit = Column(Float)  # 扣除非经常损益后的单季度净利润
    q_eps = Column(Float)  # 每股收益(单季度)
    q_netprofit_margin = Column(Float)  # 销售净利率(单季度)
    q_gsprofit_margin = Column(Float)  # 销售毛利率(单季度)
    q_exp_to_sales = Column(Float)  # 销售期间费用率(单季度)
    q_profit_to_gr = Column(Float)  # 净利润／营业总收入(单季度)
    q_saleexp_to_gr = Column(Float)  # 销售费用／营业总收入 (单季度)
    q_adminexp_to_gr = Column(Float)  # 管理费用／营业总收入 (单季度)
    q_finaexp_to_gr = Column(Float)  # 财务费用／营业总收入 (单季度)
    q_impair_to_gr_ttm = Column(Float)  # 资产减值损失／营业总收入(单季度)
    q_gc_to_gr = Column(Float)  # 营业总成本／营业总收入 (单季度)
    q_op_to_gr = Column(Float)  # 营业利润／营业总收入(单季度)
    q_roe = Column(Float)  # 净资产收益率(单季度)
    q_dt_roe = Column(Float)  # 净资产单季度收益率(扣除非经常损益)
    q_npta = Column(Float)  # 总资产净利润(单季度)
    q_opincome_to_ebt = Column(Float)  # 经营活动净收益／利润总额(单季度)
    q_investincome_to_ebt = Column(Float)  # 价值变动净收益／利润总额(单季度)
    q_dtprofit_to_profit = Column(Float)  # 扣除非经常损益后的净利润／净利润(单季度)
    q_salescash_to_or = Column(Float)  # 销售商品提供劳务收到的现金／营业收入(单季度)
    q_ocf_to_sales = Column(Float)  # 经营活动产生的现金流量净额／营业收入(单季度)
    q_ocf_to_or = Column(Float)  # 经营活动产生的现金流量净额／经营活动净收益(单季度)
    basic_eps_yoy = Column(Float)  # 基本每股收益同比增长率(%)
    dt_eps_yoy = Column(Float)  # 稀释每股收益同比增长率(%)
    cfps_yoy = Column(Float)  # 每股经营活动产生的现金流量净额同比增长率(%)
    op_yoy = Column(Float)  # 营业利润同比增长率(%)
    ebt_yoy = Column(Float)  # 利润总额同比增长率(%)
    netprofit_yoy = Column(Float)  # 归属母公司股东的净利润同比增长率(%)
    dt_netprofit_yoy = Column(Float)  # 归属母公司股东的净利润-扣除非经常损益同比增长率(%)
    ocf_yoy = Column(Float)  # 经营活动产生的现金流量净额同比增长率(%)
    roe_yoy = Column(Float)  # 净资产收益率(摊薄)同比增长率(%)
    bps_yoy = Column(Float)  # 每股净资产相对年初增长率(%)
    assets_yoy = Column(Float)  # 资产总计相对年初增长率(%)
    eqt_yoy = Column(Float)  # 归属母公司的股东权益相对年初增长率(%)
    tr_yoy = Column(Float)  # 营业总收入同比增长率(%)
    or_yoy = Column(Float)  # 营业收入同比增长率(%)
    q_gr_yoy = Column(Float)  # 营业总收入同比增长率(%)(单季度)
    q_gr_qoq = Column(Float)  # 营业总收入环比增长率(%)(单季度)
    q_sales_yoy = Column(Float)  # 营业收入同比增长率(%)(单季度)
    q_sales_qoq = Column(Float)  # 营业收入环比增长率(%)(单季度)
    q_op_yoy = Column(Float)  # 营业利润同比增长率(%)(单季度)
    q_op_qoq = Column(Float)  # 营业利润环比增长率(%)(单季度)
    q_profit_yoy = Column(Float)  # 净利润同比增长率(%)(单季度)
    q_profit_qoq = Column(Float)  # 净利润环比增长率(%)(单季度)
    q_netprofit_yoy = Column(Float)  # 归属母公司股东的净利润同比增长率(%)(单季度)
    q_netprofit_qoq = Column(Float)  # 归属母公司股东的净利润环比增长率(%)(单季度)
    equity_yoy = Column(Float)  # 净资产同比增长率
    rd_exp = Column(Float)  # 研发费用
    update_flag = Column(String(10))  # 更新标识
