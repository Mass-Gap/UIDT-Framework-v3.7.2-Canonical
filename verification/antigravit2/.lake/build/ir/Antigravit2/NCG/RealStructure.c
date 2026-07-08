// Lean compiler output
// Module: Antigravit2.NCG.RealStructure
// Imports: public import Init public meta import Init public import Mathlib.Data.Complex.Basic public import Mathlib.Algebra.Module.Basic public import Mathlib.Algebra.Star.Basic public import Mathlib.Data.ZMod.Basic
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
lean_object* lean_nat_to_int(lean_object*);
lean_object* lp_mathlib_Complex_instStarRing___lam__0(lean_object*);
lean_object* lp_mathlib_ZMod_commRing(lean_object*);
lean_object* lp_mathlib_instMulZeroClassOfSemiring___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___lam__0(lean_object*, lean_object*);
static const lean_closure_object lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___lam__0, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0_value;
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___boxed(lean_object*, lean_object*, lean_object*);
static lean_once_cell_t lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0;
static const lean_closure_object lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_mathlib_Complex_instStarRing___lam__0, .m_arity = 1, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__1 = (const lean_object*)&lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__1_value;
static lean_once_cell_t lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2;
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_trivialRealStruct;
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___lam__0(lean_object* v_self_1_, lean_object* v___y_2_){
_start:
{
lean_object* v___x_3_; 
v___x_3_ = lean_apply_1(v_self_1_, v___y_2_);
return v___x_3_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall(lean_object* v_H_5_, lean_object* v_inst_6_, lean_object* v_inst_7_){
_start:
{
lean_object* v___f_8_; 
v___f_8_ = ((lean_object*)(lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0));
return v___f_8_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___boxed(lean_object* v_H_9_, lean_object* v_inst_10_, lean_object* v_inst_11_){
_start:
{
lean_object* v_res_12_; 
v_res_12_ = lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall(v_H_9_, v_inst_10_, v_inst_11_);
lean_dec(v_inst_11_);
lean_dec_ref(v_inst_10_);
return v_res_12_;
}
}
static lean_object* _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0(void){
_start:
{
lean_object* v___x_13_; lean_object* v___x_14_; 
v___x_13_ = lean_unsigned_to_nat(8u);
v___x_14_ = lp_mathlib_ZMod_commRing(v___x_13_);
return v___x_14_;
}
}
static lean_object* _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2(void){
_start:
{
lean_object* v___x_16_; lean_object* v___x_17_; 
v___x_16_ = lean_unsigned_to_nat(1u);
v___x_17_ = lean_nat_to_int(v___x_16_);
return v___x_17_;
}
}
static lean_object* _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct(void){
_start:
{
lean_object* v___x_18_; lean_object* v_toSemiring_19_; lean_object* v___x_20_; lean_object* v_toZero_21_; lean_object* v___f_22_; lean_object* v___x_23_; lean_object* v___x_24_; 
v___x_18_ = lean_obj_once(&lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0, &lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0_once, _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__0);
v_toSemiring_19_ = lean_ctor_get(v___x_18_, 0);
lean_inc_ref(v_toSemiring_19_);
v___x_20_ = lp_mathlib_instMulZeroClassOfSemiring___redArg(v_toSemiring_19_);
v_toZero_21_ = lean_ctor_get(v___x_20_, 1);
lean_inc(v_toZero_21_);
lean_dec_ref(v___x_20_);
v___f_22_ = ((lean_object*)(lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__1));
v___x_23_ = lean_obj_once(&lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2, &lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2_once, _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct___closed__2);
v___x_24_ = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(v___x_24_, 0, v_toZero_21_);
lean_ctor_set(v___x_24_, 1, v___f_22_);
lean_ctor_set(v___x_24_, 2, v___x_23_);
lean_ctor_set(v___x_24_, 3, v___x_23_);
lean_ctor_set(v___x_24_, 4, v___x_23_);
return v___x_24_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Complex_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_Module_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_Star_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_ZMod_Basic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_antigravit2_Antigravit2_NCG_RealStructure(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Complex_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_Module_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Algebra_Star_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_ZMod_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_antigravit2_Antigravit2_NCG_trivialRealStruct = _init_lp_antigravit2_Antigravit2_NCG_trivialRealStruct();
lean_mark_persistent(lp_antigravit2_Antigravit2_NCG_trivialRealStruct);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
