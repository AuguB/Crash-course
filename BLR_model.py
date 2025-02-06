import os

import pandas as pd
from pcntoolkit.dataio.norm_data import NormData
from pcntoolkit.normative_model.norm_conf import NormConf
from pcntoolkit.normative_model.norm_hbr import NormHBR
from pcntoolkit.regression_model.hbr.hbr_conf import HBRConf
from pcntoolkit.regression_model.hbr.likelihood import NormalLikelihood
from pcntoolkit.regression_model.hbr.prior import make_prior
from pcntoolkit.util.runner import Runner
from pcntoolkit.regression_model.blr.blr_conf import BLRConf
from pcntoolkit.normative_model.norm_blr import NormBLR
import shutil

resources_dir = "/home/preclineu/stijdboe/workingdir/Projects/Crash-course/resources"
abs_path = os.path.abspath(resources_dir)
data_dir = os.path.join(abs_path, "data")
os.makedirs(data_dir, exist_ok=True)
# If you are running this notebook for the first time, you need to download the dataset from github.
# If you have already downloaded the dataset, you can comment out the following line

pd.read_csv(
    "https://raw.githubusercontent.com/predictive-clinical-neuroscience/PCNtoolkit-demo/refs/heads/main/data/fcon1000.csv"
).to_csv(os.path.join(data_dir, "fcon1000.csv"), index=False)

data = pd.read_csv(os.path.join(data_dir, "fcon1000.csv"))

covariates = ["age"]
batch_effects = ["sex", "site"]
response_vars = "lh_G_temp_sup-G_T_transv_thickness,lh_G_temp_sup-Lateral_thickness,lh_G_temp_sup-Plan_polar_thickness".split(
    ","
)

# response_vars = "lh_G&S_frontomargin_thickness,lh_G&S_occipital_inf_thickness,lh_G&S_paracentral_thickness,lh_G&S_subcentral_thickness,lh_G&S_transv_frontopol_thickness,lh_G&S_cingul-Ant_thickness,lh_G&S_cingul-Mid-Ant_thickness,lh_G&S_cingul-Mid-Post_thickness,lh_G_cingul-Post-dorsal_thickness,lh_G_cingul-Post-ventral_thickness,lh_G_cuneus_thickness,lh_G_front_inf-Opercular_thickness,lh_G_front_inf-Orbital_thickness,lh_G_front_inf-Triangul_thickness,lh_G_front_middle_thickness,lh_G_front_sup_thickness,lh_G_Ins_lg&S_cent_ins_thickness,lh_G_insular_short_thickness,lh_G_occipital_middle_thickness,lh_G_occipital_sup_thickness,lh_G_oc-temp_lat-fusifor_thickness,lh_G_oc-temp_med-Lingual_thickness,lh_G_oc-temp_med-Parahip_thickness,lh_G_orbital_thickness,lh_G_pariet_inf-Angular_thickness".split(",")
norm_data = NormData.from_dataframe(
    name="full",
    dataframe=data,
    covariates=covariates,
    batch_effects=batch_effects,
    response_vars=response_vars,
)

# Split into train and test sets

train, test = norm_data.train_test_split()
# Create a NormConf object
save_dir = os.path.join(abs_path, "save_dir")



norm_conf = NormConf(
    savemodel=True,
    saveresults=True,
    save_dir=save_dir,
    inscaler="standardize",
    outscaler="standardize",
    basis_function="bspline",
    basis_function_kwargs={"order": 3, "nknots": 5},
)

blr_conf = BLRConf(
    n_iter=100,
    intercept=True,
    random_intercept=True,
    heteroskedastic=True,
    random_intercept_var=False,
    warp="warpsinharcsinh",
    warp_reparam=False,
)

new_hbr_model = NormBLR(norm_conf=norm_conf, reg_conf=blr_conf)
sandbox_dir = os.path.join(abs_path, "runner_dir")
os.makedirs(sandbox_dir, exist_ok=True)


runner = Runner(
    cross_validate=False,
    cv_folds=3,
    parallelize=True,
    time_limit="00:10:00",
    job_type="local",
    n_jobs=2,
    log_dir=os.path.join(sandbox_dir, "log_dir"),
    temp_dir=os.path.join(sandbox_dir, "temp_dir"),
)

runner.fit_predict(new_hbr_model, train, test, observe=True)

