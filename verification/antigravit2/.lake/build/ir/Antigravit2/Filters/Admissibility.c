// Lean compiler output
// Module: Antigravit2.Filters.Admissibility
// Imports: public import Init public meta import Init public import Antigravit2.MatrixThermo.BlockPartition public import Mathlib.Data.List.Basic public import Mathlib.Tactic
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* l_List_foldl___at___00__private_Lean_Elab_MutualInductive_0__Lean_Elab_Command_isPropCandidate_spec__2(lean_object*, lean_object*);
lean_object* l_List_foldl___at___00List_min_x3f___at___00Lean_Elab_Tactic_Omega_List_nonzeroMinimum_spec__1_spec__1(lean_object*, lean_object*);
lean_object* lean_nat_sub(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_maxBlock(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_maxBlock___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_minBlock(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_minBlock___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_spread(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_spread___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2___private_Antigravit2_Filters_Admissibility_0__Antigravit2_Filters_allEqual_match__1_splitter___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2___private_Antigravit2_Filters_Admissibility_0__Antigravit2_Filters_allEqual_match__1_splitter(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_maxBlock(lean_object* v_x_1_){
_start:
{
if (lean_obj_tag(v_x_1_) == 0)
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
else
{
lean_object* v_head_3_; lean_object* v_tail_4_; lean_object* v___x_5_; 
v_head_3_ = lean_ctor_get(v_x_1_, 0);
v_tail_4_ = lean_ctor_get(v_x_1_, 1);
v___x_5_ = l_List_foldl___at___00__private_Lean_Elab_MutualInductive_0__Lean_Elab_Command_isPropCandidate_spec__2(v_head_3_, v_tail_4_);
return v___x_5_;
}
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_maxBlock___boxed(lean_object* v_x_6_){
_start:
{
lean_object* v_res_7_; 
v_res_7_ = lp_antigravit2_Antigravit2_Filters_maxBlock(v_x_6_);
lean_dec(v_x_6_);
return v_res_7_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_minBlock(lean_object* v_x_8_){
_start:
{
if (lean_obj_tag(v_x_8_) == 0)
{
lean_object* v___x_9_; 
v___x_9_ = lean_unsigned_to_nat(0u);
return v___x_9_;
}
else
{
lean_object* v_head_10_; lean_object* v_tail_11_; lean_object* v___x_12_; 
v_head_10_ = lean_ctor_get(v_x_8_, 0);
v_tail_11_ = lean_ctor_get(v_x_8_, 1);
v___x_12_ = l_List_foldl___at___00List_min_x3f___at___00Lean_Elab_Tactic_Omega_List_nonzeroMinimum_spec__1_spec__1(v_head_10_, v_tail_11_);
return v___x_12_;
}
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_minBlock___boxed(lean_object* v_x_13_){
_start:
{
lean_object* v_res_14_; 
v_res_14_ = lp_antigravit2_Antigravit2_Filters_minBlock(v_x_13_);
lean_dec(v_x_13_);
return v_res_14_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_spread(lean_object* v_xs_15_){
_start:
{
lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v___x_16_ = lp_antigravit2_Antigravit2_Filters_maxBlock(v_xs_15_);
v___x_17_ = lp_antigravit2_Antigravit2_Filters_minBlock(v_xs_15_);
v___x_18_ = lean_nat_sub(v___x_16_, v___x_17_);
lean_dec(v___x_17_);
lean_dec(v___x_16_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_Filters_spread___boxed(lean_object* v_xs_19_){
_start:
{
lean_object* v_res_20_; 
v_res_20_ = lp_antigravit2_Antigravit2_Filters_spread(v_xs_19_);
lean_dec(v_xs_19_);
return v_res_20_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2___private_Antigravit2_Filters_Admissibility_0__Antigravit2_Filters_allEqual_match__1_splitter___redArg(lean_object* v_x_21_, lean_object* v_h__1_22_, lean_object* v_h__2_23_){
_start:
{
if (lean_obj_tag(v_x_21_) == 0)
{
lean_object* v___x_24_; lean_object* v___x_25_; 
lean_dec(v_h__2_23_);
v___x_24_ = lean_box(0);
v___x_25_ = lean_apply_1(v_h__1_22_, v___x_24_);
return v___x_25_;
}
else
{
lean_object* v_head_26_; lean_object* v_tail_27_; lean_object* v___x_28_; 
lean_dec(v_h__1_22_);
v_head_26_ = lean_ctor_get(v_x_21_, 0);
lean_inc(v_head_26_);
v_tail_27_ = lean_ctor_get(v_x_21_, 1);
lean_inc(v_tail_27_);
lean_dec_ref_known(v_x_21_, 2);
v___x_28_ = lean_apply_2(v_h__2_23_, v_head_26_, v_tail_27_);
return v___x_28_;
}
}
}
LEAN_EXPORT lean_object* lp_antigravit2___private_Antigravit2_Filters_Admissibility_0__Antigravit2_Filters_allEqual_match__1_splitter(lean_object* v_motive_29_, lean_object* v_x_30_, lean_object* v_h__1_31_, lean_object* v_h__2_32_){
_start:
{
if (lean_obj_tag(v_x_30_) == 0)
{
lean_object* v___x_33_; lean_object* v___x_34_; 
lean_dec(v_h__2_32_);
v___x_33_ = lean_box(0);
v___x_34_ = lean_apply_1(v_h__1_31_, v___x_33_);
return v___x_34_;
}
else
{
lean_object* v_head_35_; lean_object* v_tail_36_; lean_object* v___x_37_; 
lean_dec(v_h__1_31_);
v_head_35_ = lean_ctor_get(v_x_30_, 0);
lean_inc(v_head_35_);
v_tail_36_ = lean_ctor_get(v_x_30_, 1);
lean_inc(v_tail_36_);
lean_dec_ref_known(v_x_30_, 2);
v___x_37_ = lean_apply_2(v_h__2_32_, v_head_35_, v_tail_36_);
return v___x_37_;
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_antigravit2_Antigravit2_MatrixThermo_BlockPartition(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_List_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_antigravit2_Antigravit2_Filters_Admissibility(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_antigravit2_Antigravit2_MatrixThermo_BlockPartition(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_List_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Tactic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
