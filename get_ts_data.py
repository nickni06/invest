# coding=utf-8
import sys
import time
import pandas as pd
import tushare as ts
'''
------------ stock basics ------------
'''
'''
获取上市所有股票信息
'''
def get_stock_basic(pro, retry_count=3, pause=2):
    """股票列表 数据"""
    frame = pd.DataFrame()
    for status in ['L', 'D', 'P']:
        for _ in range(retry_count):
            try:
                df = pro.stock_basic(exchange='', list_status=status,
                                     fields='ts_code,symbol,name,area,industry,fullname,enname,market, \
                                    exchange,curr_type,list_status,list_date,delist_date,is_hs')
                frame = frame.append(df, ignore_index=True)
            except:
                time.sleep(pause)
            else:
                break
    return frame

'''
------------ daily ------------
'''

'''
抽取日期区间内某只股票日线数据
'''
def get_daily(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date,
                           fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return df

'''
抽取单天所有股票日线数据
'''
def get_daily_date(pro, date, retry_count=3, pause=2):
    """日期方式获取 日线行情 数据"""
    for _ in range(retry_count):
        try:
            df = pro.daily(trade_date=date,
                           fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: ' + str(date) + ' updated failed! Retry count: ' + str(_) + '\n')
        else:
            return df


'''
抽取日期区间内某只股票日线数据(前复权)
'''
def get_daily_qfq(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, asset='E', adj='qfq')
        except Exception as e:
            time.sleep(pause)
            sys.stdout.write(str(e) + '\n')
            sys.stdout.write('WARNING: ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return df


'''
------------ financial info ------------
'''
'''
update income table
'''
def get_income(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,total_revenue,revenue,' \
             'int_income,prem_earned,comm_income,n_commis_income,n_oth_income,n_oth_b_income,prem_income,out_prem,' \
             'une_prem_reser,reins_income,n_sec_tb_income,n_sec_uw_income,n_asset_mg_income,oth_b_income,' \
             'fv_value_chg_gain,invest_income,ass_invest_income,forex_gain,total_cogs,oper_cost,int_exp,comm_exp,' \
             'biz_tax_surchg,sell_exp,admin_exp,fin_exp,assets_impair_loss,prem_refund,compens_payout,' \
             'reser_insur_liab,div_payt,reins_exp,oper_exp,compens_payout_refu,insur_reser_refu,reins_cost_refund,' \
             'other_bus_cost,operate_profit,non_oper_income,non_oper_exp,nca_disploss,total_profit,income_tax,n_income,' \
             'n_income_attr_p,minority_gain,oth_compr_income,t_compr_income,compr_inc_attr_p,compr_inc_attr_m_s,ebit,' \
             'ebitda,insurance_exp,undist_profit,distable_profit,update_flag'

    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            income_df = pro.income(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except Exception as e:
            time.sleep(pause)
            sys.stdout.write('WARNING: income ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
            sys.stderr.write('%s\n' %e)
        else:
            return income_df

'''
update balancesheet table
'''
def get_balancesheet(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,total_share,cap_rese,undistr_porfit,' \
             'surplus_rese,special_rese,money_cap,trad_asset,notes_receiv,accounts_receiv,oth_receiv,prepayment,' \
             'div_receiv,int_receiv,inventories,amor_exp,nca_within_1y,sett_rsrv,loanto_oth_bank_fi,premium_receiv,' \
             'reinsur_receiv,reinsur_res_receiv,pur_resale_fa,oth_cur_assets,total_cur_assets,fa_avail_for_sale,' \
             'htm_invest,lt_eqt_invest,invest_real_estate,time_deposits,oth_assets,lt_rec,fix_assets,cip,' \
             'const_materials,fixed_assets_disp,produc_bio_assets,oil_and_gas_assets,intan_assets,r_and_d,goodwill,' \
             'lt_amor_exp,defer_tax_assets,decr_in_disbur,oth_nca,total_nca,cash_reser_cb,depos_in_oth_bfi,prec_metals,' \
             'deriv_assets,rr_reins_une_prem,rr_reins_outstd_cla,rr_reins_lins_liab,rr_reins_lthins_liab,refund_depos,' \
             'ph_pledge_loans,refund_cap_depos,indep_acct_assets,client_depos,client_prov,transac_seat_fee,' \
             'invest_as_receiv,total_assets,lt_borr,st_borr,cb_borr,depos_ib_deposits,loan_oth_bank,trading_fl,' \
             'notes_payable,acct_payable,adv_receipts,sold_for_repur_fa,comm_payable,payroll_payable,taxes_payable,' \
             'int_payable,div_payable,oth_payable,acc_exp,deferred_inc,st_bonds_payable,payable_to_reinsurer,' \
             'rsrv_insur_cont,acting_trading_sec,acting_uw_sec,non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,' \
             'bond_payable,lt_payable,specific_payables,estimated_liab,defer_tax_liab,defer_inc_non_cur_liab,oth_ncl,' \
             'total_ncl,depos_oth_bfi,deriv_liab,depos,agency_bus_liab,oth_liab,prem_receiv_adva,depos_received,' \
             'ph_invest,reser_une_prem,reser_outstd_claims,reser_lins_liab,reser_lthins_liab,indept_acc_liab,' \
             'pledge_borr,indem_payable,policy_div_payable,total_liab,treasury_share,ordin_risk_reser,forex_differ,' \
             'invest_loss_unconf,minority_int,total_hldr_eqy_exc_min_int,total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,' \
             'lt_payroll_payable,oth_comp_income,oth_eqt_tools,oth_eqt_tools_p_shr,lending_funds,acc_receivable,' \
             'st_fin_payable,payables,hfs_assets,hfs_sales,update_flag'

    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            balancesheet_df = pro.balancesheet(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: balancesheet ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return balancesheet_df

'''
update cashflow table
'''
def get_cashflow(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,f_ann_date,end_date,comp_type,report_type,net_profit,finan_exp,c_fr_sale_sg,' \
             'recp_tax_rends,n_depos_incr_fi,n_incr_loans_cb,n_inc_borr_oth_fi,prem_fr_orig_contr,n_incr_insured_dep,' \
             'n_reinsur_prem,n_incr_disp_tfa,ifc_cash_incr,n_incr_disp_faas,n_incr_loans_oth_bank,n_cap_incr_repur,' \
             'c_fr_oth_operate_a,c_inf_fr_operate_a,c_paid_goods_s,c_paid_to_for_empl,c_paid_for_taxes,' \
             'n_incr_clt_loan_adv,n_incr_dep_cbob,c_pay_claims_orig_inco,pay_handling_chrg,pay_comm_insur_plcy,' \
             'oth_cash_pay_oper_act,st_cash_out_act,n_cashflow_act,oth_recp_ral_inv_act,c_disp_withdrwl_invest,' \
             'c_recp_return_invest,n_recp_disp_fiolta,n_recp_disp_sobu,stot_inflows_inv_act,c_pay_acq_const_fiolta,' \
             'c_paid_invest,n_disp_subs_oth_biz,oth_pay_ral_inv_act,n_incr_pledge_loan,stot_out_inv_act,' \
             'n_cashflow_inv_act,c_recp_borrow,proc_issue_bonds,oth_cash_recp_ral_fnc_act,stot_cash_in_fnc_act,' \
             'free_cashflow,c_prepay_amt_borr,c_pay_dist_dpcp_int_exp,incl_dvd_profit_paid_sc_ms,' \
             'oth_cashpay_ral_fnc_act,stot_cashout_fnc_act,n_cash_flows_fnc_act,eff_fx_flu_cash,n_incr_cash_cash_equ,' \
             'c_cash_equ_beg_period,c_cash_equ_end_period,c_recp_cap_contrib,incl_cash_rec_saims,uncon_invest_loss,' \
             'prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,lt_amort_deferred_exp,decr_deferred_exp,' \
             'incr_acc_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,invest_loss,decr_def_inc_tax_assets,' \
             'incr_def_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,others,' \
             'im_net_cashflow_oper_act,conv_debt_into_cap,conv_copbonds_due_within_1y,fa_fnc_leases,end_bal_cash,' \
             'beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,im_n_incr_cash_equ,update_flag'

    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            cashflow_df = pro.cashflow(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: cashflow ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return cashflow_df


'''
update forecast table
'''
def get_forecast(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,end_date,type,p_change_min,p_change_max,net_profit_min,net_profit_max,last_parent_net,' \
             'first_ann_date'  # ,summary,change_reason'

    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            df = pro.forecast(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: forecast ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return df

'''
update express table
'''
def get_express(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,end_date,revenue,operate_profit,total_profit,n_income,total_assets,' \
             'total_hldr_eqy_exc_min_int,diluted_eps,diluted_roe,yoy_net_profit,bps,yoy_sales,yoy_op,yoy_tp,' \
             'yoy_dedu_np,yoy_eps,yoy_roe,growth_assets,yoy_equity,growth_bps,or_last_year,op_last_year,' \
             'tp_last_year,np_last_year,eps_last_year,open_net_assets,open_bps,perf_summary,is_audit,remark'
    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            df = pro.express(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: express ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return df

'''
update fina_indicator table
'''
def get_fina_indicator(pro, ts_code, start_date, end_date, retry_count=3, pause=2):
    fields = 'ts_code,ann_date,end_date,eps,dt_eps,total_revenue_ps,revenue_ps,capital_rese_ps,surplus_rese_ps,' \
             'undist_profit_ps,extra_item,profit_dedt,gross_margin,current_ratio,quick_ratio,cash_ratio,invturn_days,' \
             'arturn_days,inv_turn,ar_turn,ca_turn,fa_turn,assets_turn,op_income,valuechange_income,interst_income,daa,' \
             'ebit,ebitda,fcff,fcfe,current_exint,noncurrent_exint,interestdebt,netdebt,tangible_asset,working_capital,' \
             'networking_capital,invest_capital,retained_earnings,diluted2_eps,bps,ocfps,retainedps,cfps,ebit_ps,' \
             'fcff_ps,fcfe_ps,netprofit_margin,grossprofit_margin,cogs_of_sales,expense_of_sales,profit_to_gr,' \
             'saleexp_to_gr,adminexp_of_gr,finaexp_of_gr,impai_ttm,gc_of_gr,op_of_gr,ebit_of_gr,roe,roe_waa,roe_dt,' \
             'roa,npta,roic,roe_yearly,roa2_yearly,roe_avg,opincome_of_ebt,investincome_of_ebt,n_op_profit_of_ebt,' \
             'tax_to_ebt,dtprofit_to_profit,salescash_to_or,ocf_to_or,ocf_to_opincome,capitalized_to_da,debt_to_assets,' \
             'assets_to_eqt,dp_assets_to_eqt,ca_to_assets,nca_to_assets,tbassets_to_totalassets,int_to_talcap,' \
             'eqt_to_talcapital,currentdebt_to_debt,longdeb_to_debt,ocf_to_shortdebt,debt_to_eqt,eqt_to_debt,' \
             'eqt_to_interestdebt,tangibleasset_to_debt,tangasset_to_intdebt,tangibleasset_to_netdebt,ocf_to_debt,' \
             'ocf_to_interestdebt,ocf_to_netdebt,ebit_to_interest,longdebt_to_workingcapital,ebitda_to_debt,turn_days,' \
             'roa_yearly,roa_dp,fixed_assets,profit_prefin_exp,non_op_profit,op_to_ebt,nop_to_ebt,ocf_to_profit,' \
             'cash_to_liqdebt,cash_to_liqdebt_withinterest,op_to_liqdebt,op_to_debt,roic_yearly,total_fa_trun,' \
             'profit_to_op,q_opincome,q_investincome,q_dtprofit,q_eps,q_netprofit_margin,q_gsprofit_margin,' \
             'q_exp_to_sales,q_profit_to_gr,q_saleexp_to_gr,q_adminexp_to_gr,q_finaexp_to_gr,q_impair_to_gr_ttm,' \
             'q_gc_to_gr,q_op_to_gr,q_roe,q_dt_roe,q_npta,q_opincome_to_ebt,q_investincome_to_ebt,q_dtprofit_to_profit,' \
             'q_salescash_to_or,q_ocf_to_sales,q_ocf_to_or,basic_eps_yoy,dt_eps_yoy,cfps_yoy,op_yoy,ebt_yoy,netprofit_yoy,' \
             'dt_netprofit_yoy,ocf_yoy,roe_yoy,bps_yoy,assets_yoy,eqt_yoy,tr_yoy,or_yoy,q_gr_yoy,q_gr_qoq,q_sales_yoy,' \
             'q_sales_qoq,q_op_yoy,q_op_qoq,q_profit_yoy,q_profit_qoq,q_netprofit_yoy,q_netprofit_qoq,equity_yoy,rd_exp,' \
             'update_flag'

    """股票代码方式获取 日线行情 数据"""
    for count in range(retry_count):
        try:
            df = pro.fina_indicator(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
        except:
            time.sleep(pause)
            sys.stdout.write('WARNING: fina_indicator ' + str(ts_code) + ' updated failed! Retry count: ' + str(count) + '\n')
        else:
            return df
