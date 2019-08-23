#ifndef __QUERY_H___
#define __QUERY_H___

int query_help(int exit_code);

void redir(char* fl_nm);

void print_query_result_offset(uint32_t *mask,
                               uint32_t mask_len,
                               uint32_t *vids,
                               struct gqt_query *q,
                               uint32_t **counts,
                               uint32_t *id_lens,
                               uint32_t *U_R,
                               uint32_t U_R_len,
                               char **id_query_list,
                               char **gt_query_list,
                               uint32_t num_qs,
                               uint32_t num_fields,
                               char *off_file_name,
                               char *source_file,
                               char *full_cmd);

void print_query_result_bim(uint32_t *mask,
                        uint32_t mask_len,
                        uint32_t *vids,
                        struct gqt_query *q,
                        uint32_t **counts,
                        uint32_t *id_lens,
                        uint32_t num_qs,
                        uint32_t num_fields,
                        char *bim,
                        char *full_cmd);
int query_cmp(uint32_t value,
              int op_condition,
              int condition_value);


#if 0
void get_bcf_query_result(uint32_t *mask,
                        uint32_t mask_len,
                        struct gqt_query *q,
                        char **id_query_list,
                        uint32_t *id_lens,
                        uint32_t num_qs,
                        uint32_t num_fields,
                        char *vid_file_name,
                        char *bcf_file_name,
                        int bcf_output);
#endif

int compare_uint32_t (const void *a, const void *b);

int query(int argc, char **argv, char *full_cmd);
#endif