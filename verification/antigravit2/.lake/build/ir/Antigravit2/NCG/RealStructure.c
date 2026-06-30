// Lean compiler output
// Module: Antigravit2.NCG.RealStructure
// Imports: public import Init public meta import Init public import Mathlib.Data.Complex.Basic public import Mathlib.Algebra.Module.Basic public import Mathlib.Algebra.Star.Basic
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
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___lam__0(lean_object*, lean_object*);
static const lean_closure_object lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___lam__0, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___closed__0_value;
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_instCoeFunAntiLinearMapForall___boxed(lean_object*, lean_object*, lean_object*);
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
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Complex_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_Module_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Algebra_Star_Basic(uint8_t builtin);
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
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
