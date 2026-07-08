// Lean compiler output
// Module: Antigravit2.MatrixThermo.BlockPartition
// Imports: public import Init public meta import Init public import Mathlib.Data.List.Basic public import Mathlib.Data.Nat.Basic public import Mathlib.Tactic
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
lean_object* lp_mathlib_List_sum___at___00Composition_sizeUpTo_spec__0(lean_object*);
lean_object* lean_nat_mul(lean_object*, lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* l_List_lengthTR___redArg(lean_object*);
lean_object* l_List_reverse___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_List_mapTR_loop___at___00Antigravit2_MatrixThermo_entropyList_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropyList(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagList___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___boxed(lean_object*, lean_object*);
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__0_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__0_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__1 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__1_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p21 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__1_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__0_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__0_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__1 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__1_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p22 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__1_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p321___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__1_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p321___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p321___closed__0_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p321 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p321___closed__0_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(1) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p21___closed__0_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__0_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__0_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__1 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__1_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__1_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__2 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__2_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p2211 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p2211___closed__2_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__0_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(3) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__0_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__1 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__1_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p33 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p33___closed__1_value;
static const lean_ctor_object lp_antigravit2_Antigravit2_MatrixThermo_p222___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)(((size_t)(2) << 1) | 1)),((lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p22___closed__1_value)}};
static const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p222___closed__0 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p222___closed__0_value;
LEAN_EXPORT const lean_object* lp_antigravit2_Antigravit2_MatrixThermo_p222 = (const lean_object*)&lp_antigravit2_Antigravit2_MatrixThermo_p222___closed__0_value;
LEAN_EXPORT lean_object* lp_antigravit2_List_mapTR_loop___at___00Antigravit2_MatrixThermo_entropyList_spec__0(lean_object* v_a_1_, lean_object* v_a_2_){
_start:
{
if (lean_obj_tag(v_a_1_) == 0)
{
lean_object* v___x_3_; 
v___x_3_ = l_List_reverse___redArg(v_a_2_);
return v___x_3_;
}
else
{
lean_object* v_head_4_; lean_object* v_tail_5_; lean_object* v___x_7_; uint8_t v_isShared_8_; uint8_t v_isSharedCheck_14_; 
v_head_4_ = lean_ctor_get(v_a_1_, 0);
v_tail_5_ = lean_ctor_get(v_a_1_, 1);
v_isSharedCheck_14_ = !lean_is_exclusive(v_a_1_);
if (v_isSharedCheck_14_ == 0)
{
v___x_7_ = v_a_1_;
v_isShared_8_ = v_isSharedCheck_14_;
goto v_resetjp_6_;
}
else
{
lean_inc(v_tail_5_);
lean_inc(v_head_4_);
lean_dec(v_a_1_);
v___x_7_ = lean_box(0);
v_isShared_8_ = v_isSharedCheck_14_;
goto v_resetjp_6_;
}
v_resetjp_6_:
{
lean_object* v___x_9_; lean_object* v___x_11_; 
v___x_9_ = lean_nat_mul(v_head_4_, v_head_4_);
lean_dec(v_head_4_);
if (v_isShared_8_ == 0)
{
lean_ctor_set(v___x_7_, 1, v_a_2_);
lean_ctor_set(v___x_7_, 0, v___x_9_);
v___x_11_ = v___x_7_;
goto v_reusejp_10_;
}
else
{
lean_object* v_reuseFailAlloc_13_; 
v_reuseFailAlloc_13_ = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(v_reuseFailAlloc_13_, 0, v___x_9_);
lean_ctor_set(v_reuseFailAlloc_13_, 1, v_a_2_);
v___x_11_ = v_reuseFailAlloc_13_;
goto v_reusejp_10_;
}
v_reusejp_10_:
{
v_a_1_ = v_tail_5_;
v_a_2_ = v___x_11_;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropyList(lean_object* v_xs_15_){
_start:
{
lean_object* v___x_16_; lean_object* v___x_17_; lean_object* v___x_18_; 
v___x_16_ = lean_box(0);
v___x_17_ = lp_antigravit2_List_mapTR_loop___at___00Antigravit2_MatrixThermo_entropyList_spec__0(v_xs_15_, v___x_16_);
v___x_18_ = lp_mathlib_List_sum___at___00Composition_sizeUpTo_spec__0(v___x_17_);
lean_dec(v___x_17_);
return v___x_18_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(lean_object* v_x_19_){
_start:
{
if (lean_obj_tag(v_x_19_) == 0)
{
lean_object* v___x_20_; 
v___x_20_ = lean_unsigned_to_nat(0u);
return v___x_20_;
}
else
{
lean_object* v_head_21_; lean_object* v_tail_22_; lean_object* v___x_23_; lean_object* v___x_24_; lean_object* v___x_25_; lean_object* v___x_26_; 
v_head_21_ = lean_ctor_get(v_x_19_, 0);
v_tail_22_ = lean_ctor_get(v_x_19_, 1);
v___x_23_ = lp_mathlib_List_sum___at___00Composition_sizeUpTo_spec__0(v_tail_22_);
v___x_24_ = lean_nat_mul(v_head_21_, v___x_23_);
lean_dec(v___x_23_);
v___x_25_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(v_tail_22_);
v___x_26_ = lean_nat_add(v___x_24_, v___x_25_);
lean_dec(v___x_25_);
lean_dec(v___x_24_);
return v___x_26_;
}
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagList___boxed(lean_object* v_x_27_){
_start:
{
lean_object* v_res_28_; 
v_res_28_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(v_x_27_);
lean_dec(v_x_27_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___redArg(lean_object* v_p_29_){
_start:
{
lean_object* v___x_30_; 
v___x_30_ = l_List_lengthTR___redArg(v_p_29_);
return v___x_30_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___redArg___boxed(lean_object* v_p_31_){
_start:
{
lean_object* v_res_32_; 
v_res_32_ = lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___redArg(v_p_31_);
lean_dec(v_p_31_);
return v_res_32_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks(lean_object* v_N_33_, lean_object* v_p_34_){
_start:
{
lean_object* v___x_35_; 
v___x_35_ = l_List_lengthTR___redArg(v_p_34_);
return v___x_35_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks___boxed(lean_object* v_N_36_, lean_object* v_p_37_){
_start:
{
lean_object* v_res_38_; 
v_res_38_ = lp_antigravit2_Antigravit2_MatrixThermo_BlockPartition_numBlocks(v_N_36_, v_p_37_);
lean_dec(v_p_37_);
lean_dec(v_N_36_);
return v_res_38_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy___redArg(lean_object* v_p_39_){
_start:
{
lean_object* v___x_40_; 
v___x_40_ = lp_antigravit2_Antigravit2_MatrixThermo_entropyList(v_p_39_);
return v___x_40_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy(lean_object* v_N_41_, lean_object* v_p_42_){
_start:
{
lean_object* v___x_43_; 
v___x_43_ = lp_antigravit2_Antigravit2_MatrixThermo_entropyList(v_p_42_);
return v___x_43_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_entropy___boxed(lean_object* v_N_44_, lean_object* v_p_45_){
_start:
{
lean_object* v_res_46_; 
v_res_46_ = lp_antigravit2_Antigravit2_MatrixThermo_entropy(v_N_44_, v_p_45_);
lean_dec(v_N_44_);
return v_res_46_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___redArg(lean_object* v_p_47_){
_start:
{
lean_object* v___x_48_; 
v___x_48_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(v_p_47_);
return v___x_48_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___redArg___boxed(lean_object* v_p_49_){
_start:
{
lean_object* v_res_50_; 
v_res_50_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___redArg(v_p_49_);
lean_dec(v_p_49_);
return v_res_50_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty(lean_object* v_N_51_, lean_object* v_p_52_){
_start:
{
lean_object* v___x_53_; 
v___x_53_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagList(v_p_52_);
return v___x_53_;
}
}
LEAN_EXPORT lean_object* lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty___boxed(lean_object* v_N_54_, lean_object* v_p_55_){
_start:
{
lean_object* v_res_56_; 
v_res_56_ = lp_antigravit2_Antigravit2_MatrixThermo_offDiagPenalty(v_N_54_, v_p_55_);
lean_dec(v_p_55_);
lean_dec(v_N_54_);
return v_res_56_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_List_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Data_Nat_Basic(uint8_t builtin);
lean_object* initialize_mathlib_Mathlib_Tactic(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_antigravit2_Antigravit2_MatrixThermo_BlockPartition(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_List_Basic(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_mathlib_Mathlib_Data_Nat_Basic(builtin);
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
