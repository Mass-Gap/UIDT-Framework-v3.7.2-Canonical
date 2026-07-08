// Lean compiler output
// Module: Antigravit2.NCG.FiniteAlgebra
// Imports: public import Init public meta import Init public import Antigravit2.NCG.RealStructure public import Mathlib.Data.ZMod.Basic
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
lean_object* lp_mathlib_ZMod_commRing(lean_object*);
lean_object* lp_mathlib_instMulZeroClassOfSemiring___redArg(lean_object*);
static lean_once_cell_t lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0;
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra;
static lean_object* _init_lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0(void){
_start:
{
lean_object* v___x_1_; lean_object* v___x_2_; 
v___x_1_ = lean_unsigned_to_nat(8u);
v___x_2_ = lp_mathlib_ZMod_commRing(v___x_1_);
return v___x_2_;
}
}
static lean_object* _init_lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra(void){
_start:
{
lean_object* v___x_3_; lean_object* v_toSemiring_4_; lean_object* v___x_5_; lean_object* v_toZero_6_; lean_object* v___x_8_; uint8_t v_isShared_9_; uint8_t v_isSharedCheck_14_; 
v___x_3_ = lean_obj_once(&lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0, &lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0_once, _init_lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra___closed__0);
v_toSemiring_4_ = lean_ctor_get(v___x_3_, 0);
lean_inc_ref(v_toSemiring_4_);
v___x_5_ = lp_mathlib_instMulZeroClassOfSemiring___redArg(v_toSemiring_4_);
v_toZero_6_ = lean_ctor_get(v___x_5_, 1);
v_isSharedCheck_14_ = !lean_is_exclusive(v___x_5_);
if (v_isSharedCheck_14_ == 0)
{
lean_object* v_unused_15_; 
v_unused_15_ = lean_ctor_get(v___x_5_, 0);
lean_dec(v_unused_15_);
v___x_8_ = v___x_5_;
v_isShared_9_ = v_isSharedCheck_14_;
goto v_resetjp_7_;
}
else
{
lean_inc(v_toZero_6_);
lean_dec(v___x_5_);
v___x_8_ = lean_box(0);
v_isShared_9_ = v_isSharedCheck_14_;
goto v_resetjp_7_;
}
v_resetjp_7_:
{
lean_object* v___x_10_; lean_object* v___x_12_; 
v___x_10_ = lean_unsigned_to_nat(1u);
if (v_isShared_9_ == 0)
{
lean_ctor_set(v___x_8_, 1, v___x_10_);
lean_ctor_set(v___x_8_, 0, v_toZero_6_);
v___x_12_ = v___x_8_;
goto v_reusejp_11_;
}
else
{
lean_object* v_reuseFailAlloc_13_; 
v_reuseFailAlloc_13_ = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(v_reuseFailAlloc_13_, 0, v_toZero_6_);
lean_ctor_set(v_reuseFailAlloc_13_, 1, v___x_10_);
v___x_12_ = v_reuseFailAlloc_13_;
goto v_reusejp_11_;
}
v_reusejp_11_:
{
return v___x_12_;
}
}
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_antigravit2_Antigravit2_NCG_RealStructure(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_ZMod_Basic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_antigravit2_Antigravit2_NCG_FiniteAlgebra(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_antigravit2_Antigravit2_NCG_RealStructure(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_ZMod_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra = _init_lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra();
lean_mark_persistent(lp_antigravit2_Antigravit2_NCG_trivialFiniteAlgebra);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
